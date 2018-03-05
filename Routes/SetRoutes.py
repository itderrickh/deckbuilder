from flask import Flask, request, send_from_directory, Response, Blueprint
from Models.CardSet import CardSet
from AppState.Session import ses
from flask.json import jsonify

set_routes = Blueprint('set_routes', __name__,
                        template_folder='templates')

@set_routes.route("/api/sets/", methods=['GET'])
def get_sets():
	res = ses.query(CardSet).all()
	d = set()
	for x in res:
		d.add(x.setName)

	return jsonify(list(d))