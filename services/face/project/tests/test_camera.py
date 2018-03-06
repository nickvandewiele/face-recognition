
import os
import unittest

from project.tests.base import BaseTestCase

from project.api.camera import Camera

class TestCamera(BaseTestCase):

    def test_create_camera_path(self):
        '''Test if Camera can be instantiated from a video file.'''
        camera = Camera(path='test.mp4')
        self.assertIsNotNone(camera.video)

    def test_create_camera_path_none(self):
        '''Test if Camera can be instantiated for streaming purposes.'''
        camera = Camera()
        self.assertIsNotNone(camera.video)

    def test_get_frame(self):
        '''Test if Camera.get_frame returns an object.'''
        camera = Camera()
        jpeg_bytes = camera.get_frame()
        self.assertIsNotNone(jpeg_bytes)        

if __name__ == '__main__':
    unittest.main()