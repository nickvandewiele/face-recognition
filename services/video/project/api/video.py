import numpy as np

from flask import Blueprint, jsonify, request, render_template, Response, redirect, url_for

video_blueprint = Blueprint('video', __name__, template_folder='./templates')

from project.api.camera import Camera, gen

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
    if request.method == 'POST':
        return take_pic()

    return render_template('index.html')


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

