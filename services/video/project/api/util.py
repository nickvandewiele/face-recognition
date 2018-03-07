import requests

def call_face(image):
    '''call the face container to recognize an identity in the image.'''

    url = 'http://face:5000/'

    payload = {'image': image.tolist()}

    response = requests.post(url, json=payload)

    return response