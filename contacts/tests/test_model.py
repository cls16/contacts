from contacts.app import db
from contacts.model import Contact, User

class TestContact:

    def setup(self):
        Contact.query.delete()
        db.session.commit()

    def test_add(self):
        bob = Contact(firstname='bob', lastname='smith', 
        email='bsmith@example.com', phonenumber='555-555-5555')
        db.session.add(bob)
        db.session.commit()

        contact = Contact.query.one()
        assert contact.firstname == 'bob'

class TestUser:

    def setup(self):
        Contact.query.delete()
        db.session.commit()

    def test_add(self):
        bob = User(username='bob', password='foobar')
        db.session.add(bob)
        db.session.commit()

        user = User.query.one()
        assert user.username == 'bob'

    def test_validate(self):

        assert not User.validate('foo', 'bar')

        bob = User(username='foo', password='bar')
        db.session.add(bob)
        db.session.commit()

        assert User.validate('foo', 'bar')