
import os
import unittest
import json
import numpy as np
import cv2

from project.tests.base import BaseTestCase
from project.api.face import load_model, populate_db, who_is_it

class TestFace(BaseTestCase):


    def test_load_db(self):
        '''test if we can populate the database with an image.'''

        FRmodel = load_model()
        db = populate_db(FRmodel = FRmodel)
        self.assertIn('nick', db.keys())


    def test_who_is_it(self):
        '''test if who is it works.'''
        FRmodel = load_model()
        database = populate_db(FRmodel = FRmodel)
        fn = os.path.join('project', 'api', 'images', 'nick_96.JPG')
        min_dist, identity = who_is_it(fn, database, FRmodel)

        self.assertEqual(identity, 'nick')


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
