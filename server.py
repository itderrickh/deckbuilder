import os
from flask import Flask, request, send_from_directory
from flask.json import jsonify
from flask_jwt import JWT, current_identity, jwt_required
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from AppState.Session import ses
from Helpers.DeckLib import create_deck_list, get_deck_from_source, get_deck_from_limitless_tcg
from Helpers.Seed import seed
from Models.Card import Card
from Models.Deck import Deck
from Models.User import User
from datetime import timedelta
from scipy.stats import hypergeom

app = Flask(__name__)
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'wwwroot')
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=14400)

seed()

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
	''' Serves the static index file '''
	return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
	''' Serves the wwwroot files '''
	if not os.path.isfile(os.path.join(static_file_dir, path)):
		path = os.path.join(path, 'index.html')

	return send_from_directory(static_file_dir, path)

def authenticate(username, password):
	user = ses.query(User).filter(User.username==username).first()
	if user and pbkdf2_sha256.verify(password, user.password):
		return user

def identity(payload):
	user_id = payload['identity']
	user = ses.query(User).filter(User.id==user_id).first()
	return user

jwt = JWT(app, authenticate, identity)

@app.errorhandler(404)
def page_not_found(error):
	print(error)
	return jsonify({ 'message': 'Error'}), 404

@app.route("/api/decks/", methods=['GET'])
@jwt_required()
def get_decks():
	res = ses.query(Deck).filter(Deck.userId==current_identity.id).all()
	return jsonify(Deck.serialize_list(res))

@app.route("/api/decks/import", methods=['POST'])
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

@app.route("/api/decks/import/limitless", methods=['POST'])
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

@app.route("/api/sets/", methods=['GET'])
def get_sets():
	res = ses.query(Card).all()
	d = set()
	for x in res:
		d.add(x.setName)

	return jsonify(list(d))

@app.route("/api/decks/<deckid>", methods=['GET'])
@jwt_required()
def get_deck(deckid):
	res = ses.query(Deck).filter(Deck.id==deckid and current_identity.id == Deck.userId).first()
	return jsonify(res.serialize())

@app.route("/api/cards/deck/<deckid>", methods=['GET'])
@jwt_required()
def get_cards(deckid):
	res = ses.query(Card).filter(Card.deckId==deckid).all()
	return jsonify(Card.serialize_list(res))

@app.route("/api/cards/deck/export/<deckid>", methods=['GET'])
@jwt_required()
def get_cards_export(deckid):
	res = ses.query(Card).filter(Card.deckId==deckid).all()

	return jsonify({ 'deck': Card.serialize_list(res), 'text': create_deck_list(res)})

@app.route("/api/deck/bulk", methods=['POST'])
@jwt_required()
def create_deck_bulk():
	content = request.get_json()
	deck = Deck(name=content['name'], userId=current_identity.id)
	ses.add(deck)
	ses.commit()

	for value in content['deck']:
		ses.add(Card(name=value['name'],count=value['count'],setName=value['setName'],type=value['type'],deckId=deck.id,number=value['number']))

	return jsonify({ }), 204

@app.route("/api/draw/<decksize>/<targets>/<drawn>", methods=['GET'])
def draw_calc(decksize, targets, drawn):
	hpd = hypergeom(int(decksize), int(targets), int(drawn))
	li = [hpd.pmf(c) for c in range(1,int(drawn))]
	return jsonify({ 'result': sum(li) })

if __name__ == '__main__':
	app.run()
