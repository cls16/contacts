import flask_webtest
from app import app


class TestWeb:
    @classmethod
    def setup_class(self):
        self.app = app
        self.app.testing = True
        self.client = flask_webtest.TestApp(self.app)

    def test_hello_world(self):
        resp = self.client.get('/')
        doc = resp.pyquery

        assert 'Hello' in doc('title').text()
        assert 'Hello World!' in doc('body').text()
