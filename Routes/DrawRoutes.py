from flask import Blueprint, render_template, abort
from flask_jwt import JWT, current_identity, jwt_required
from scipy.stats import hypergeom
from flask.json import jsonify

draw_routes = Blueprint('draw_routes', __name__,
                        template_folder='templates')

@draw_routes.route("/api/draw/<decksize>/<targets>/<drawn>", methods=['GET'])
def draw_calc(decksize, targets, drawn):
	hpd = hypergeom(int(decksize), int(targets), int(drawn))
	li = [hpd.pmf(c) for c in range(1,int(drawn))]
	return jsonify({ 'result': sum(li) })