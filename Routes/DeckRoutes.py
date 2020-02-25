from flask import Blueprint, render_template, abort, request, send_file, after_this_request
from flask_jwt import JWT, current_identity, jwt_required
from Models.Deck import Deck
from Models.Card import Card
from Models.DeckCard import DeckCard
from Models.CardSet import CardSet
from flask.json import jsonify
from AppState.Session import ses, ElasticStore
from Helpers.DeckLib import create_deck_list, get_deck_from_source, get_deck_from_limitless_tcg
from Helpers.WritePdf import write_to_pdf
from Helpers.Deckmin import get_shared_decklist, print_deck
import uuid
import os
import time
import copy
from threading import Thread
import random
import urllib
import json
from Helpers.UrlOpener import MyOpener, DOWNLOADS_DIR, download_cards_if_not_exists
from Helpers.SetHelper import getSet, getSetCode

pdf_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../pdfgen')
deck_routes = Blueprint('deck_routes', __name__,
						template_folder='templates')

@deck_routes.route("/api/deck/bulk", methods=['POST'])
@jwt_required()
def create_deck_bulk():
	content = request.get_json()
	deck = Deck(name=content['name'], userId=current_identity.id, sprites=";".join(content['sprites']))
	ses.add(deck)
	ses.commit()

	cards = {x:content['deck'].count(x) for x in content['deck']}
	for value in cards.keys():
		ses.add(DeckCard(deckId=deck.id,cardId=value,count=cards[value]))

	return jsonify({ }), 204

@deck_routes.route("/api/decks/<deckid>", methods=['GET'])
@jwt_required()
def get_deck(deckid):
	res = ses.query(Deck).filter(Deck.id==deckid, current_identity.id == Deck.userId).first()
	return jsonify(res.serialize())

@deck_routes.route("/api/decks/", methods=['GET'])
@jwt_required()
def get_decks():
	res = ses.query(Deck).filter(Deck.userId==current_identity.id).all()
	return jsonify(Deck.serialize_list(res))

@deck_routes.route("/api/decks/hand/<deckid>", methods=['GET'])
@jwt_required()
def get_sample_hand(deckid):
	cards = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	cardIds = [r.cardId for r in cards]
	fullDeck = list()

	finalCards = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(cardIds)).all())
	for card in finalCards:
		countOfCard = next(r.count for r in cards if card.Id==r.cardId)
		for _ in range(countOfCard):
			fullDeck.append(card)

	download_cards_if_not_exists(finalCards)

	random.shuffle(fullDeck)
	lastList = fullDeck[:7]
	return jsonify(Card.serialize_list(lastList))

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

@deck_routes.route("/api/decks/import", methods=['POST'])
@jwt_required()
def add_deck():
	content = request.get_json()
	deck_list = get_deck_from_source(content['text'])
	sets = ses.query(CardSet).all()
	deck = Deck(name=content['name'], userId=current_identity.id, sprites=";".join(content['sprites']))

	try:
		ses.add(deck)
		ses.flush()

		for _, value in deck_list.items():
			if "{*}" in value['card']:
				value['card'] = value['card'].replace("{*}", "Prism Star")
			if "◇" in value['card']:
				value['card'] = value['card'].replace("◇", "Prism Star")
			if value['type'] == "Energy":
				if "Energy" not in value['card']:
					value['card'] += " Energy"
				card = ses.query(Card).filter(Card.name==value['card']).order_by(Card.Id.desc()).first()
			else:
				card = ses.query(Card).filter(Card.name==value['card'], Card.setName==getSet(sets, value['set']), Card.number==value['number']).first()

			if card is None:
				print(value['card'])
				cards = ElasticStore.search(index="card-index", body={"size": 1, "query": {"match": { "name": value['card'] }}})
				card = Struct(**cards['hits']['hits'][0]['_source'])

			ses.add(DeckCard(deckId=deck.id,cardId=card.Id,count=value['count']))

		ses.commit()
	except:
		ses.rollback()
		raise


	return jsonify({ 'deck': deck.serialize() }), 201

@deck_routes.route("/api/decks/import/limitless", methods=['POST'])
@jwt_required()
def import_limitless_deck():
	content = request.get_json()
	deck_list = get_deck_from_limitless_tcg(content['url'])
	sets = ses.query(CardSet).all()
	deck = Deck(name=content['name'], userId=current_identity.id, sprites=";".join(content['sprites']))

	try:
		ses.add(deck)
		ses.flush()

		for _, value in deck_list.items():
			if "{*}" in value['card']:
				value['card'].replace("{*}", "Prism Star")
			if "◇" in value['card']:
				value['card'].replace("◇", "Prism Star")
			if value['type'] == "Energy":
				if "Energy" not in value['card']:
					value['card'] += " Energy"
				card = ses.query(Card).filter(Card.name==value['card']).order_by(Card.Id.desc()).first()
			else:
				card = ses.query(Card).filter(Card.name==value['card'], Card.setName==getSet(sets, value['set']), Card.number==value['number']).first()

			if card is None:
				print(value['card'])
				cards = ElasticStore.search(index="card-index", body={"size": 1, "query": {"match": { "name": value['card'] }}})
				card = cards['hits']['hits'][0]['_source']
			ses.add(DeckCard(deckId=deck.id,cardId=card.Id,count=value['count']))

		ses.commit()
	except:
		ses.rollback()
		raise

	return jsonify({ 'deck': deck.serialize() }), 201

@deck_routes.route("/api/deck/exportpdf/<deckid>", methods=['GET'])
@jwt_required()
def export_pdf(deckid):
	c1 = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	dcOneIds = [r.cardId for r in c1]
	d1 = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(dcOneIds)).all())
	sets = ses.query(CardSet).all()

	for card in d1:
		card.count = next(r.count for r in c1 if card.Id==r.cardId)
		if card.type != "Energy":
			card.setName = getSetCode(sets, card.setName)
	uid = str(uuid.uuid4())
	outfile, warnings = write_to_pdf(d1, current_identity, uid + '.pdf')
	return jsonify({ 'pdffile': uid, 'warnings': warnings }), 201

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
def deck_min(deckOneId, deckTwoId):
	c1 = ses.query(DeckCard).filter(DeckCard.deckId==deckOneId).all()
	c2 = ses.query(DeckCard).filter(DeckCard.deckId==deckTwoId).all()
	dcOneIds = [r.cardId for r in c1]
	dcTwoIds = [r.cardId for r in c2]

	d1 = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(dcOneIds)).all())
	d2 = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(dcTwoIds)).all())

	for card in d1:
		card.count = next(r.count for r in c1 if card.Id==r.cardId)

	for card in d2:
		card.count = next(r.count for r in c2 if card.Id==r.cardId)

	shared, deck1, deck2 = get_shared_decklist(d1, d2)

	slim_deck_one = {x:y for x, y in deck1.items() if y != 0}
	slim_deck_two = {x:y for x, y in deck2.items() if y != 0}

	return jsonify({ 'deckOne': slim_deck_one, 'deckTwo': slim_deck_two, 'shared': shared }), 201

def delay_delete(delay, path):
	time.sleep(delay)
	os.remove(path)
	return