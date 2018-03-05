from flask import Blueprint, render_template, abort, request, send_file, after_this_request
from flask_jwt import JWT, current_identity, jwt_required
from Models.Deck import Deck
from Models.Card import Card
from flask.json import jsonify
from AppState.Session import ses
from Helpers.DeckLib import create_deck_list, get_deck_from_source, get_deck_from_limitless_tcg
from writepdf import write_to_pdf
from Helpers.Deckmin import get_shared_decklist, print_deck
import uuid
import os
import time
from threading import Thread

pdf_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../pdfgen')
deck_routes = Blueprint('deck_routes', __name__,
                        template_folder='templates')

@deck_routes.route("/api/deck/bulk", methods=['POST'])
@jwt_required()
def create_deck_bulk():
	content = request.get_json()
	deck = Deck(name=content['name'], userId=current_identity.id)
	ses.add(deck)
	ses.commit()

	for value in content['deck']:
		ses.add(Card(name=value['name'],count=value['count'],setName=value['setName'],type=value['type'],deckId=deck.id,number=value['number']))

	return jsonify({ }), 204

@deck_routes.route("/api/decks/<deckid>", methods=['GET'])
@jwt_required()
def get_deck(deckid):
	res = ses.query(Deck).filter(Deck.id==deckid and current_identity.id == Deck.userId).first()
	return jsonify(res.serialize())

@deck_routes.route("/api/decks/", methods=['GET'])
@jwt_required()
def get_decks():
	res = ses.query(Deck).filter(Deck.userId==current_identity.id).all()
	return jsonify(Deck.serialize_list(res))

@deck_routes.route("/api/decks/import", methods=['POST'])
@jwt_required()
def add_deck():
	content = request.get_json()
	deck_list = get_deck_from_source(content['text'])

	deck = Deck(name=content['name'], userId=current_identity.id)
	ses.add(deck)
	ses.commit()

	for _, value in deck_list.items():
		ses.add(Card(name=value['card'],count=value['count'],setName=value['set'],type=value['type'],deckId=deck.id,number=value['number']))

	ses.commit()

	return jsonify({ 'deck': deck.serialize() }), 201

@deck_routes.route("/api/decks/import/limitless", methods=['POST'])
@jwt_required()
def import_limitless_deck():
	content = request.get_json()
	deck_list = get_deck_from_limitless_tcg(content['url'])

	deck = Deck(name=content['name'], userId=current_identity.id)
	ses.add(deck)
	ses.commit()

	for _, value in deck_list.items():
		ses.add(Card(name=value['card'],count=value['count'],setName=value['set'],type=value['type'],deckId=deck.id,number=value['number']))

	ses.commit()

	return jsonify({ 'deck': deck.serialize() }), 201

@deck_routes.route("/api/deck/exportpdf/<deckid>", methods=['GET'])
@jwt_required()
def export_pdf(deckid):
	res = ses.query(Card).filter(Card.deckId==deckid).all()
	uid = str(uuid.uuid4())
	outfile = write_to_pdf(res, current_identity, uid + '.pdf')
	return jsonify({ 'pdffile': uid }), 201

@deck_routes.route("/api/pdf/<pdfid>", methods=['GET'])
def one_time_pdf(pdfid):
	if os.path.isfile(os.path.join(pdf_file_dir, pdfid + '.pdf')):
		resp = send_file(os.path.join(pdf_file_dir, pdfid + '.pdf'), attachment_filename=pdfid + '.pdf')
		del_thread = Thread(target=delay_delete, args=(5, os.path.join(pdf_file_dir, pdfid + '.pdf')))
		del_thread.start()
		return resp
	else:
		resp = ('', 404)
		return resp

@deck_routes.route("/api/deck/deckmin/<deckOneId>/<deckTwoId>", methods=['GET'])
@jwt_required()
def deck_min(deckOneId, deckTwoId):
	d1 = ses.query(Card).filter(Card.deckId==deckOneId).all()
	d2 = ses.query(Card).filter(Card.deckId==deckTwoId).all()
	shared, deck1, deck2 = get_shared_decklist(d1, d2)

	slim_deck_one = {x:y for x, y in deck1.items() if y != 0}
	slim_deck_two = {x:y for x, y in deck2.items() if y != 0}

	return jsonify({ 'deckOne': slim_deck_one, 'deckTwo': slim_deck_two, 'shared': shared }), 201

def delay_delete(delay, path):
	time.sleep(delay)
	os.remove(path)
	return