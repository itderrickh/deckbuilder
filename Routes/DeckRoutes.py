from flask import Blueprint, render_template, abort
from flask_jwt import JWT, current_identity, jwt_required

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