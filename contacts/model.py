from contacts.app import db
from flask_login import UserMixin


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.firstname, self.lastname, self.phonenumber


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.username, self.password

    @classmethod
    def validate(cls, username, password):
        return cls.query.filter_by(username=username, password=password).one_or_none()

    @classmethod
    def testing_create(cls):
        user = cls(username='foo', password='bar')
        db.session.add(user)
        db.session.commit()
        return user