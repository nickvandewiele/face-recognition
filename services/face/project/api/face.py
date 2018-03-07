import os
import numpy as np

from .recognize import load_model, populate_db, recognize

from flask import Blueprint, jsonify, request, render_template, Response, redirect, url_for

face_blueprint = Blueprint('face', __name__, template_folder='./templates')

@face_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success from face!',
        'message': 'pong!'
    })


@face_blueprint.route('/', methods=['POST'])    
def main():

    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.',
        'name': '',
    }

    post_data = request.get_json()

    if not post_data:
        return jsonify(response_object), 400

    image = post_data.get('image')
    image = np.array(image, dtype=np.uint8)

    FRmodel = load_model()
    database = populate_db(FRmodel = FRmodel)
    min_dist, identity = recognize(image, database, FRmodel)

    if identity is not None:
        
        response_object = {
                'status': 'success',
                'name': identity,
            }

        return jsonify(response_object), 200
    else:
        response_object = {
                'status': 'fail',
                'message': 'Could not recognize identity.',
            }
        return jsonify(response_object), 400
