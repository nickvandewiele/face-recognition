
import os
import unittest
import numpy as np
import cv2

from project.tests.base import BaseTestCase

from project.api.camera import Camera, save_picture

class TestCamera(BaseTestCase):

    def test_create_camera_path(self):
        '''Test if Camera can be instantiated from a video file.'''
        fn = os.path.join('project', 'tests', 'test.mp4')
        camera = Camera(path=fn)
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
        self.assertEqual(image.dtype, np.uint8)

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

    def test_read_video(self):
        '''test if video can be succesfully read.'''
        
        fn = os.path.join('project', 'tests', 'test.mp4')
        camera = Camera(path=fn) # from video
        img = camera.read_video()

        self.assertIsNotNone(img)

    def test_resize(self):
        '''test if image resizing works as expected.'''

        fn = os.path.join('project', 'tests', 'nick_large.JPG')
        image = cv2.imread(fn, 1)

        img_resized = cv2.resize(image, (96, 96))
        img_np = np.array(img_resized, dtype=np.uint8)
        self.assertEqual(img_np.shape, (96, 96, 3))

    def test_take_picture_and_resize(self):
        '''test if we can take a picture and resize it to specific size.'''

        camera = Camera() # from video source
        shape = (96, 96)
        image = camera.take_picture_and_resize(shape=shape)

        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (96, 96, 3))
        self.assertEqual(image.dtype, np.uint8)


if __name__ == '__main__':
    unittest.main()