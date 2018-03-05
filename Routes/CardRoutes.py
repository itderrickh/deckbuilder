from flask import Blueprint, render_template, abort
from flask_jwt import JWT, current_identity, jwt_required
from flask.json import jsonify
from AppState.Session import ses
from Models.Card import Card
from Helpers.DeckLib import create_deck_list

card_routes = Blueprint('card_routes', __name__,
                        template_folder='templates')

@card_routes.route("/api/cards/deck/<deckid>", methods=['GET'])
@jwt_required()
def get_cards(deckid):
	res = ses.query(Card).filter(Card.deckId==deckid).all()
	return jsonify(Card.serialize_list(res))

@card_routes.route("/api/cards/deck/export/<deckid>", methods=['GET'])
@jwt_required()
def get_cards_export(deckid):
	res = ses.query(Card).filter(Card.deckId==deckid).all()

	return jsonify({ 'deck': Card.serialize_list(res), 'text': create_deck_list(res)})