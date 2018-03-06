import os
import numpy as np

from .fr_utils import load_weights_from_FaceNet, img_to_encoding, img_to_encoding2
from .inception_blocks_v2 import faceRecoModel


from flask import Blueprint, jsonify, request, render_template, Response, redirect, url_for

face_blueprint = Blueprint('face', __name__, template_folder='./templates')

def load_model():
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    print("Total Params:", FRmodel.count_params())

    load_weights_from_FaceNet(FRmodel)

    return FRmodel

FRmodel = load_model()

@face_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
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

def populate_db(FRmodel):
    database = {}
    fn = os.path.join('project', 'api', 'images', 'nick_96.JPG')
    database["nick"] = img_to_encoding(fn, FRmodel)

    return database

def who_is_it(image_path, database, model):
    """
    Arguments:
    image_path -- path to an image
    database -- database containing image encodings along with the name of the person on the image
    model -- your Inception model instance in Keras
    
    Returns:
    min_dist -- the minimum distance between image_path encoding and the encodings from the database
    identity -- string, the name prediction for the person on image_path
    """
        
    ## Step 1: Compute the target "encoding" for the image. Use img_to_encoding() see example above. ## (≈ 1 line)
    encoding = img_to_encoding(image_path, model)
    
    ## Step 2: Find the closest encoding ##
    
    # Initialize "min_dist" to a large value, say 100 (≈1 line)
    min_dist = 100
    
    # Loop over the database dictionary's names and encodings.
    for (name, db_enc) in database.items():
        
        # Compute L2 distance between the target "encoding" and the current "emb" from the database. (≈ 1 line)
        dist = np.linalg.norm(encoding - db_enc)

        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. (≈ 3 lines)
        if dist < min_dist:
            min_dist = dist
            identity = name
    
    if min_dist > 0.7:
        print("Not in the database.")
    else:
        print ("it's " + str(identity) + ", the distance is " + str(min_dist))
        
    return min_dist, identity

def recognize(image, database, model):
    """
    Arguments:
    image -- image (numpy array)
    database -- database containing image encodings along with the name of the person on the image
    model -- your Inception model instance in Keras
    
    Returns:
    min_dist -- the minimum distance between image_path encoding and the encodings from the database
    identity -- string, the name prediction for the person on image_path
    """
        
    ## Step 1: Compute the target "encoding" for the image. Use img_to_encoding() see example above. ## (≈ 1 line)
    encoding = img_to_encoding2(image, model)
    
    ## Step 2: Find the closest encoding ##
    
    # Initialize "min_dist" to a large value, say 100 (≈1 line)
    min_dist = 100
    
    # Loop over the database dictionary's names and encodings.
    for (name, db_enc) in database.items():
        
        # Compute L2 distance between the target "encoding" and the current "emb" from the database. (≈ 1 line)
        dist = np.linalg.norm(encoding - db_enc)

        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. (≈ 3 lines)
        if dist < min_dist:
            min_dist = dist
            identity = name
    
    if min_dist > 0.7:
        print("Not in the database.")
    else:
        print ("it's " + str(identity) + ", the distance is " + str(min_dist))
        
    return min_dist, identity