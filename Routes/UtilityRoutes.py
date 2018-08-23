from flask import Flask, request, send_from_directory, Response, Blueprint
from AppState.Session import ses
from Models.Event import Event
from flask.json import jsonify
from flask_jwt import JWT, current_identity, jwt_required
import requests
import json
from datetime import datetime, timedelta
from lxml import html

util_routes = Blueprint('util_routes', __name__,
						template_folder='templates')

def get_events():
	future_date = datetime.utcnow() + timedelta(weeks=4)
	current_date = datetime.utcnow() - timedelta(days=1)
	return ses.query(Event).filter(Event.date < future_date, Event.date > current_date).all()

def get_list_from_official(url):
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
			event = Event(name=content[2], location=content[3], status=content[4], date=datetime.strptime(content[5], "%b %d, %Y %I:%M%p"))
			# Prevent duplicate events and cache existing events
			if ses.query(Event).filter(Event.name==event.name, Event.date==event.date).count() == 0:
				ses.add(event)
	ses.commit()

	return get_events()

@util_routes.route("/api/events", methods=['GET'])
@util_routes.route("/api/events/<refresh>", methods=['GET'])
def get_home(refresh="false"):
	zipCode = '54904'
	if current_identity is not None:
		zipCode = current_identity.zipCode
	url = "https://www.pokemon.com/us/play-pokemon/pokemon-events/find-an-event/?country=176&postal_code={}&city=&event_name=&location_name=&address=&state_object=&state_other=&distance_within=100&start_date=0&end_date=30&event_type=league&event_type=tournament&event_type=premier&product_type=tcg&product_type=vg&sort_order=when&results_pp=100".format(zipCode)
	if refresh == "true":
		res = get_list_from_official(url)
	else:
		res = get_events()
	return jsonify(Event.serialize_list(res))
