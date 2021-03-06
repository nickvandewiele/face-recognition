
import os
import unittest
import json
import numpy as np
import cv2

from project.tests.base import BaseTestCase
from project.api.recognize import populate_db, who_is_it
from project.api.util import load_model


class TestRecognize(BaseTestCase):


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

if __name__ == '__main__':
    unittest.main()
