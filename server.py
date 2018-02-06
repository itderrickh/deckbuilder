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
from Routes.DeckRoutes import deck_routes
from Routes.CardRoutes import card_routes
from Routes.DrawRoutes import draw_routes

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

@app.route("/api/sets/", methods=['GET'])
def get_sets():
	res = ses.query(Card).all()
	d = set()
	for x in res:
		d.add(x.setName)

	return jsonify(list(d))

app.register_blueprint(card_routes)
app.register_blueprint(deck_routes)
app.register_blueprint(draw_routes)

if __name__ == '__main__':
	app.run()
