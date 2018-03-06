
import os
import unittest
import numpy as np
import cv2

from project.tests.base import BaseTestCase

from project.api.camera import Camera, save_picture

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

    def test_get_picture(self):
        '''Test if Camera can take a picture.'''

        camera = Camera() # from video source
        image = camera.take_picture()
        
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (480, 640, 3)) # dimensions of my webcam images

    def test_save_picture(self):
        '''Test if we can save a picture to file.'''
        
        rgb_color=(0, 0, 0)
        image = np.zeros((100, 100, 3), np.uint8)# Create black blank image

        # Since OpenCV uses BGR, convert the color first
        color = tuple(reversed(rgb_color))
        # Fill image with color
        image[:] = color

        fn = 'face.jpg'
        save_picture(image, path=fn)
        self.assertTrue(os.path.isfile(fn))

        os.remove(fn)


if __name__ == '__main__':
    unittest.main()