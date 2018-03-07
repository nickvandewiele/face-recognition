
import os
import unittest
import json
import numpy as np
import requests
import cv2

from project.tests.base import BaseTestCase
from flask import Response

class TestVideoService(BaseTestCase):

    def test_ping(self):
        '''test if /ping route works.'''
        response = self.client.get('/ping')

        data = json.loads(response.data.decode())

        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_video_feed(self):
        '''test if /video_feed route returns Response.'''
        response = self.client.get('/video_feed')

        self.assertTrue(isinstance(response, Response))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'multipart/x-mixed-replace')

    def test_main_get(self):
        '''test that get works for the main route.'''
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Take a picture</h1>', response.data)
        self.assertIn(b'<h1>Detected face:</h1>', response.data)
        self.assertIn(b'<p>No faces!</p>', response.data)

    def test_main_post(self):
        '''test that the post method works for the main route.'''

        response = self.client.post('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Take a picture</h1>', response.data)
        self.assertIn(b'<h1>Detected face:</h1>', response.data)
        self.assertIn(b'nick', response.data)


    def test_take_picture(self):
        '''test that the take_pic route works and sends correct json data.'''
        
        response = self.client.get('/take_pic')
        data = json.loads(response.data.decode())

        image = np.array(data['image'], dtype=np.uint8)

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertIn('image was taken!', data['message'])
        
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (96, 96, 3))
        self.assertEqual(image.dtype, np.uint8)

if __name__ == '__main__':
    unittest.main()
    