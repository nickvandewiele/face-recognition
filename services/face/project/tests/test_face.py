
import os
import unittest
import json
import numpy as np
import cv2

from project.tests.base import BaseTestCase
from project.api.recognize import populate_db, who_is_it
from project.api.util import load_model


class TestFace(BaseTestCase):

    def test_ping(self):
        '''test if /ping route works.'''
        response = self.client.get('/ping')

        data = json.loads(response.data.decode())

        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


    def test_main_post(self):
        '''test that posting an image works for the main route.'''

        fn = os.path.join('project', 'api', 'images', 'nick_96.JPG')
        image = cv2.imread(fn, 1)

        with self.client:
            response = self.client.post(
                '/',
                data=json.dumps({
                    'image': image.tolist()
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('nick', data['name'])


if __name__ == '__main__':
    unittest.main()
