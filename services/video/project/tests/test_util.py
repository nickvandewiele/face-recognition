
import os
import unittest
import json
import cv2
import requests

from project.tests.base import BaseTestCase

from project.api.video import call_face

class TestUtil(BaseTestCase):

    def test_call_face_ping(self):
        '''test if video container can ping face container'''

        url = 'http://face:5000/ping'
        response = requests.get(url)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('face', data['status'])

    def test_call_face_main(self):
        '''test if video container can post an image on the main route of face container'''

        fn = os.path.join('project', 'tests', 'nick_96.JPG')
        image = cv2.imread(fn, 1)

        url = 'http://face:5000/'
        payload = {'image': image.tolist()}

        response = requests.post(url, json=payload)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertIn('nick', data['name'])


    def test_call_face(self):
        '''test if "call face" method can be correctly used. '''

        fn = os.path.join('project', 'tests', 'nick_96.JPG')
        image = cv2.imread(fn, 1)

        response = call_face(image)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertIn('nick', data['name'])


if __name__ == '__main__':
    unittest.main()
    