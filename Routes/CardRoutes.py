from flask import Blueprint, render_template, abort, request
from flask_jwt import JWT, current_identity, jwt_required
from flask.json import jsonify
from AppState.Session import ses
from Models.Card import Card
from Models.CardSet import CardSet
from Models.DeckCard import DeckCard
from Helpers.DeckLib import create_deck_list

card_routes = Blueprint('card_routes', __name__,
                        template_folder='templates')

def getSet(sets, setName):
	return next((s.setName for s in sets if s.name == setName), "")

@card_routes.route("/api/cards/deck/<deckid>", methods=['GET'])
@jwt_required()
def get_cards(deckid):
	res = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	dcIds = [r.cardId for r in res]
	cards = ses.query(Card).filter(Card.Id.in_(dcIds)).all()
	sets = ses.query(CardSet).all()

	for card in cards:
		card.count = next(r.count for r in res if card.Id==r.cardId)
		if card.type != "Energy":
			print(card.name)
			card.setName = getSet(sets, card.setName)
	return jsonify(Card.serialize_list(cards))

@card_routes.route("/api/cards/deck/export/<deckid>", methods=['GET'])
@jwt_required()
def get_cards_export(deckid):
	res = ses.query(DeckCard).filter(DeckCard.deckId==deckid).all()
	dcIds = [r.cardId for r in res]
	cards = ses.query(Card).filter(Card.Id.in_(dcIds)).all()
	sets = ses.query(CardSet).all()

	for card in cards:
		card.count = next(r.count for r in res if card.Id==r.cardId)
		if card.type != "Energy":
			card.setName = getSet(sets, card.setName)
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