from unittest import TestCase

import requests
from sqlalchemy import create_engine

from core.models.base import install_model


class AppTestCase(TestCase):
    test_url = ''

    def test_get(self):
        self.assertEqual(1+1, 2)

    def test_post(self):
        self.assertEqual(1+1, 2)

    def test_put(self):
        self.assertEqual(1+1, 2)

    def test_delete(self):
        self.assertEqual(1+1, 2)
