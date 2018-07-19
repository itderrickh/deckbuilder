import os
from datetime import datetime
from flask import Flask, request, send_from_directory, Response
from flask.json import jsonify
from flask_jwt import JWT, current_identity, jwt_required
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from AppState.Session import ses
from Helpers.DeckLib import create_deck_list, get_deck_from_source, get_deck_from_limitless_tcg
from Helpers.Seed import seed
from Models.User import User
from datetime import timedelta
from Routes.DeckRoutes import deck_routes
from Routes.CardRoutes import card_routes
from Routes.DrawRoutes import draw_routes
from Routes.StaticRoutes import static_routes
from Routes.SetRoutes import set_routes
from Routes.UtilityRoutes import util_routes

app = Flask(__name__, static_folder = './wwwroot')
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=14400)

seed()

def authenticate(username, password):
	user = ses.query(User).filter(User.username==username).first()
	if user and pbkdf2_sha256.verify(password, user.password):
		return user

def identity(payload):
	user_id = payload['user_id']
	user = ses.query(User).filter(User.id==user_id).first()
	return user

jwt = JWT(app, authenticate, identity)

@jwt.jwt_payload_handler
def make_payload(identity):
    return {
		'user_id': identity.id,
		'theme': identity.theme,
		'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA'],
		'iat': datetime.utcnow(),
		'nbf': datetime.utcnow()
	}

@app.errorhandler(404)
def page_not_found(error):
	print(error)
	return jsonify({ 'message': 'Error', 'error': str(error) }), 404

@app.errorhandler(500)
def error_handler(error):
	print(error)
	return jsonify({ 'message': 'Error', 'error': str(error) }), 500

@app.route('/api/register', methods=['POST'])
def register():
	content = request.get_json()

	if(ses.query(User).filter(User.username==content['username']).count() > 0):
		return jsonify({ 'error': 'This user already exists. Please enter a new username.'}), 500
	else:
		user = User(
			name=content['name'],
			username=content['username'],
			password=pbkdf2_sha256.hash(content['password']),
			playerid=content['playerid'],
			dateofbirth=datetime.strptime(content['dateofbirth'], "%Y-%m-%dT%H:%M:%S.%fZ" ),
			theme=content['theme']
		)

		ses.add(user)
		ses.commit()
		return jsonify({ 'message': 'User successfully created. Please login to continue.' })

@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

app.register_blueprint(static_routes)
app.register_blueprint(set_routes)
app.register_blueprint(card_routes)
app.register_blueprint(deck_routes)
app.register_blueprint(draw_routes)
app.register_blueprint(util_routes)

if __name__ == '__main__':
	app.run()
