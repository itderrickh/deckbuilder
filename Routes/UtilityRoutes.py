from flask import Flask, request, send_from_directory, Response, Blueprint
from AppState.Session import ses
from Models.Event import Event
from Models.UserEvent import UserEvent
from flask.json import jsonify
from flask_jwt import JWT, current_identity, jwt_required
import requests
import json
from datetime import datetime, timedelta
from lxml import html

util_routes = Blueprint('util_routes', __name__,
						template_folder='templates')

def get_events(start, end):
	if start is not None and end is not None:
		return ses.query(Event).filter(Event.date < datetime.strptime(end, '%Y-%m-%d'), Event.date > datetime.strptime(start, '%Y-%m-%d')).all()
	else:
		future_date = datetime.utcnow() + timedelta(weeks=12)
		current_date = datetime.utcnow() - timedelta(days=1)
		return ses.query(Event).filter(Event.date < future_date, Event.date > current_date).all()


def get_list_from_official(url, start, end):
	''' Get deck from url provided '''
	page = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
	tree = html.fromstring(page.content)

	# Get the value of the table
	columns = tree.xpath('//*[@id="table-1"]/tbody/tr')
	for c in columns:
		content = list()
		for i in c.iterchildren():
			content.append(i.text_content().strip())
		if len(content) == 7 and (content[0] == "Pokémon TCG" or content[0] == "ALL"):
			event = Event(title=content[2], location=content[3], status=content[4], date=datetime.strptime(content[5], "%b %d, %Y %I:%M%p"))
			# Prevent duplicate events and cache existing events
			if ses.query(Event).filter(Event.title==event.title, Event.date==event.date, Event.location==event.location).count() == 0:
				ses.add(event)
	ses.commit()

	return get_events(start, end)

@util_routes.route("/api/events", methods=['GET'])
@util_routes.route("/api/events/<refresh>", methods=['GET'])
def get_home(refresh="false"):
	zipCode = '54904'
	if current_identity:
		zipCode = current_identity.zipCode
	url = "https://www.pokemon.com/us/play-pokemon/pokemon-events/find-an-event/?country=176&postal_code={}&city=&event_name=&location_name=&address=&state_object=&state_other=&distance_within=250&start_date=0&end_date=90&event_type=tournament&event_type=premier&product_type=tcg&sort_order=when&results_pp=100".format(zipCode)
	if refresh == "true":
		res = get_list_from_official(url, request.args.get('start'), request.args.get('end'))
	else:
		res = get_events(request.args.get('start'), request.args.get('end'))
	return jsonify(Event.serialize_list(res))

@util_routes.route("/api/2.0/events/hide", methods=['POST'])
@jwt_required()
def add_hidden_user_events():
	content = request.get_json()
	if len(ses.query(UserEvent.id).filter(UserEvent.userId==current_identity.id, UserEvent.eventId==content['eventId']).all()) <= 0:
		uevent = UserEvent(userId=current_identity.id, eventId=content['eventId'], hidden=True, attended=False, points=0, meta="")
		ses.add(uevent)
		ses.commit()
		return jsonify(uevent.serialize())
	else:
		return jsonify({ 'error': 'Event already has been modified'}), 500

@util_routes.route("/api/2.0/events/add", methods=['POST'])
@jwt_required()
def add_user_events():
	content = request.get_json()
	if len(ses.query(UserEvent.id).filter(UserEvent.userId==current_identity.id, UserEvent.eventId==content['eventId']).all()) <= 0:
		uevent = UserEvent(userId=current_identity.id, eventId=content['eventId'], hidden=False, attended=False, points=0, meta="")
		ses.add(uevent)
		ses.commit()
		return jsonify(uevent.serialize())
	else:
		return jsonify({ 'error': 'Event already has been modified'}), 500

@util_routes.route("/api/2.0/events/user", methods=['GET'])
@jwt_required()
def get_user_current_events():
	user_events = ses.query(UserEvent.eventId).filter(UserEvent.userId==current_identity.id, UserEvent.hidden==False).all()
	user_events_ids = [value for value, in user_events]
	events = get_events(request.args.get('start'), request.args.get('end'))
	events = ses.query(Event).filter(Event.id.in_(user_events_ids))

	return jsonify(Event.serialize_list(events))

@util_routes.route("/api/2.0/events/", methods=['GET'])
@util_routes.route("/api/2.0/events/<refresh>", methods=['GET'])
@jwt_required()
def get_user_events(refresh="false"):
	zipCode = '54904'
	if current_identity:
		zipCode = current_identity.zipCode
	url = "https://www.pokemon.com/us/play-pokemon/pokemon-events/find-an-event/?country=176&postal_code={}&city=&event_name=&location_name=&address=&state_object=&state_other=&distance_within=250&start_date=0&end_date=90&event_type=tournament&event_type=premier&product_type=tcg&sort_order=when&results_pp=100".format(zipCode)
	user_events = ses.query(UserEvent.eventId).filter(UserEvent.userId==current_identity.id).all()
	user_events_ids = [value for value, in user_events]
	if refresh == "true":
		events = get_list_from_official(url, request.args.get('start'), request.args.get('end'))
		events = ses.query(Event).filter(Event.id.notin_(user_events_ids))
	else:
		events = get_events(request.args.get('start'), request.args.get('end'))
		events = ses.query(Event).filter(Event.id.notin_(user_events_ids))

	return jsonify(Event.serialize_list(events))
