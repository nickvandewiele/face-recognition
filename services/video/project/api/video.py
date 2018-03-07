import os
import json
import numpy as np
import cv2

from flask import Blueprint, jsonify, request, render_template, Response, redirect, url_for

video_blueprint = Blueprint('video', __name__, template_folder='./templates')

from project.api.camera import Camera, gen
from project.api.util import call_face

@video_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success from video!',
        'message': 'pong!'
    })

@video_blueprint.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@video_blueprint.route('/', methods=['GET', 'POST'])    
def main():

    name = ''

    if request.method == 'POST':

        # take picture
        response, status_code = take_pic()

        data = json.loads(response.data.decode())

        success = data.get('status')
        assert 'success' in success, 'Something went wrong while taking a picture..'

        # convert image into numpy array
        image = data.get('image')
        image = np.array(image, dtype=np.uint8)

        # send picture for face recognition

        fn = os.path.join('project', 'tests', 'nick_96.JPG')
        image = cv2.imread(fn, 1)

        response = call_face(image)
        post_data = response.json()

        success = post_data.get('status')
        assert 'success' in success, 'Something went wrong while recognizing faces..'

        name = post_data.get('name')


    return render_template('index.html', face=name)


@video_blueprint.route('/take_pic', methods=['GET'])    
def take_pic():
    '''take a picture, with the Camera object, send the resulting numpy array.'''

    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.',
        'image': np.zeros((480, 640, 3), dtype=np.uint8).tolist(),
    }

    try:
        image = Camera().take_picture()

        response_object = {
                    'status': 'success',
                    'message': 'image was taken!',
                    'image': image.tolist(),
                }

        return jsonify(response_object), 200
    except:
        pass

    return jsonify(response_object), 400