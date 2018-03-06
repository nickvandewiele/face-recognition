
import os
import unittest
import json

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

	def test_main(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertIn(b'<h1>Take a picture</h1>', response.data)