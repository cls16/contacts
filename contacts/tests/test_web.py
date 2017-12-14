import flask_webtest
from contacts.app import app


class TestWeb:
    @classmethod
    def setup_class(self):
        self.app = app
        self.app.testing = True
        self.client = flask_webtest.TestApp(self.app)

    def test_hello_world(self):
        resp = self.client.get('/')
        doc = resp.pyquery

        assert 'Hello' == doc('title').text()
        assert 'Hello World!' == doc('body').text()

    def test_hello_caleb(self):
        resp = self.client.get('/?name=caleb')
        doc = resp.pyquery

        assert 'Hello caleb!' == doc('body').text()

    def test_form(self):
        resp = self.client.get('/')

        form = resp.form
        form['name'] = 'caleb'
        resp = form.submit()
        doc = resp.pyquery

        assert 'Hello caleb!' == doc('body').text()
