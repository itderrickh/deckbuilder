from flask import Flask, request, send_from_directory, Response, Blueprint
import os

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../wwwroot')

static_routes = Blueprint('static_routes', __name__,
                        template_folder='templates')

@static_routes.route('/', methods=['GET'])
def serve_dir_directory_index():
	''' Serves the static index file '''
	return send_from_directory(static_file_dir, 'index.html')

@static_routes.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
	''' Serves the wwwroot files '''
	if not os.path.isfile(os.path.join(static_file_dir, path)):
		path = os.path.join(path, 'index.html')

	return send_from_directory(static_file_dir, path)
