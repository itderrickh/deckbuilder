from flask import Flask, request, send_from_directory, Response, Blueprint
from Models.CardSet import CardSet
from Models.Card import Card
from AppState.Session import ses, ElasticStore
from flask.json import jsonify
from werkzeug.utils import secure_filename
import os
import glob
import json

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Data/json/cards/')
ALLOWED_EXTENSIONS = set(['json'])

set_routes = Blueprint('set_routes', __name__,
                        template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@set_routes.route("/api/sets/", methods=['GET'])
def get_sets():
	res = ses.query(CardSet).all()
	d = set()
	for x in res:
		d.add(x.setName)

	return jsonify(list(d))

@set_routes.route("/api/sets/upload", methods=['POST'])
def add_sets_json():
	# check if the post request has the file part
	if 'file' not in request.files:
		print('No file part')
		return jsonify({ 'error': 'No file part'})
	file = request.files['file']
	# if user does not select file, browser also
	# submit a empty part without filename
	if file.filename == '':
		print('No selected file')
		return jsonify({ 'error': 'No file part'})
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		for item in glob.glob(os.path.join(UPLOAD_FOLDER, filename)):
			print(filename)
			with open(item, encoding="utf8") as f:
				data = json.load(f)
				for d in data:
					card = Card(
						name=d['name'].encode('UTF-8'),
						subtype=d.get('subtype'),
						type=d.get('supertype'),
						evolvesFrom=d.get('evolvesFrom', '').encode('UTF-8'),
						ability=d.get('ability'),
						hp=int(d.get('hp') if str(d.get('hp')) != "None" else 0),
						retreatCost=d.get('convertedRetreatCost'),
						artist=d['artist'],
						rarity=d.get('rarity'),
						setName=d['series'] + " - " + d['set'],
						setCode=d['setCode'],
						types=d.get('types'),
						localImageUrl="/" + d['setCode'] + "/" + d.get('number') + ".png",
						imageUrl=d.get('imageUrl'),
						attacks=d.get('attacks'),
						weaknesses=d.get('weaknesses'),
						number=d['number'])
					ses.add(card)
					ses.flush()
					ElasticStore.index(index="card-index", doc_type='card', id=card.Id, body=card.serialize())
			ses.commit()
	return jsonify({ 'success': True})