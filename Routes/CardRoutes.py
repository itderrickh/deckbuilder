from flask import Blueprint, render_template, abort, request
from flask_jwt import JWT, current_identity, jwt_required
from flask.json import jsonify
from AppState.Session import ses, ElasticStore
from Models.Card import Card
from Models.CardSet import CardSet
from Models.DeckCard import DeckCard
from Helpers.DeckLib import create_deck_list
import copy
import requests
import os
import urllib
from Helpers.UrlOpener import MyOpener, DOWNLOADS_DIR, download_cards_if_not_exists
from Helpers.SetHelper import getSetCode

card_routes = Blueprint('card_routes', __name__,
                        template_folder='templates')

@card_routes.route("/api/cards/deck/<deckid>", methods=['GET'])
@jwt_required()
def get_cards(deckid):
	res = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	dcIds = [r.cardId for r in res]
	cards = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(dcIds)).all())
	sets = ses.query(CardSet).all()

	download_cards_if_not_exists(cards)
	for card in cards:
		card.count = next(r.count for r in res if card.Id==r.cardId)
		if card.type != "Energy":
			card.setName = getSetCode(sets, card.setName)
	return jsonify(Card.serialize_list(cards))

@card_routes.route("/api/cards/deck/export/<deckid>", methods=['GET'])
@jwt_required()
def get_cards_export(deckid):
	res = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	dcIds = [r.cardId for r in res]
	cards = copy.deepcopy(ses.query(Card).filter(Card.Id.in_(dcIds)).all())
	sets = ses.query(CardSet).all()

	for card in cards:
		card.count = next(r.count for r in res if card.Id==r.cardId)
		if card.type != "Energy":
			card.setName = getSetCode(sets, card.setName)
	return jsonify({ 'deck': Card.serialize_list(cards), 'text': create_deck_list(cards)})

@card_routes.route("/api/cards", methods=['GET'])
def get_all_cards():
	limit = request.args.get('limit', 50)
	offset = request.args.get('offset', 0)
	res = ses.query(Card).limit(limit).offset(offset).all()
	return jsonify({ 'cards': Card.serialize_list(res) })

@card_routes.route("/api/cards/<cardId>", methods=['GET'])
def get_card_by_id(cardId):
	res = ses.query(Card).filter(Card.Id==cardId).first()
	return jsonify(Card.serialize(res))

@card_routes.route("/api/cards/search/<name>", methods=['GET'])
def search_by_name(name):
	res = ElasticStore.search(index="card-index", body={"size": 100, "query": {"match_phrase_prefix": { "name": name }}})
	myopener = MyOpener()

	#Download files if we don't have them already
	#	Reduces future hits to the API
	for hit in res['hits']['hits']:
		directory = os.path.join(DOWNLOADS_DIR, hit['_source']['setCode'])
		filename = os.path.join(DOWNLOADS_DIR, *hit['_source']['localImageUrl'].split("/"))
		if not os.path.exists(directory):
			os.makedirs(directory)

		if not os.path.isfile(filename):
			myopener.retrieve(hit['_source']['imageUrl'], filename)

	return jsonify(res)