import unittest
import random
import string
import hashlib

from werkzeug.test import Client

from mvmusic.api.app import create_app


class BaseClientTest(unittest.TestCase):
    version = "1.14.0"

    def setUp(self):
        app = create_app()
        self.client = Client(app)

    def make_request(self, view_name, **kwargs):
        user = "testuser"
        password = "testpassword"

        symbols = string.ascii_lowercase + string.digits
        salt = ''.join(random.choices(symbols, k=6))
        token = hashlib.md5(f"{password}{salt}".encode()).hexdigest()

        params = {
            "u": user,
            "t": token,
            "s": salt,
            "c": "unittest",
            "v": self.version,
            "f": "json"
        }

        params.update(kwargs)

        return self.client.post(f"/rest/{view_name}.view", data=params)
