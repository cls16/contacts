from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import contacts.validation as val

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.firstname, self.lastname, self.phonenumber

db.drop_all()
db.create_all()

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/addcontact', methods=['GET', 'POST'])
def addcontact():
    if request.method == 'POST':
        result = val.ContactSchema().load(request.form)
        if result.errors:
            return render_template('form.html', error_messages=result.errors, values=request.form)
        else:
            form_firstname=request.form['firstname']
            newcontact = Contact(firstname=form_firstname, lastname=request.form['lastname'], 
            email=request.form['email'], phonenumber=request.form['phonenumber'])
            db.session.add(newcontact)
            db.session.commit()
            return redirect(url_for('contacts'))
    elif request.method == 'GET':
        return render_template('form.html', values = {}, message='Please enter your contact information below.')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        ids = request.form.getlist('contact_id')
        Contact.query.filter(Contact.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return redirect(url_for('contacts'))
    elif request.method == 'GET':
        return render_template('contacts.html', contacts=Contact.query.all())

#create database
#db.create_all()
# #create users
# admin = User(username='admin', email='admin@example.com')
# guest = User(username='guest', email='guest@example.net')
# #add users
# db.session.add(admin)
# db.session.add(guest)
# #commit changes
# db.session.commit()
# print('ADMIN USER:' + str(User.query.filter_by(username='admin').first()))
# #create python category
# py = Category(name='Python')
# """There are two posts below. The first post is created already within the python category 
#     using 'category=py'. The second post is created (as a variable). Then it is appended to
#     the python category on the next line. I guess these are just two different ways of 
#     doing it, each more useful in its own situation."""
# #1st post
# Post(title='Hello Python!', body='Python is pretty cool', category=py)
# #2nd post
# p = Post(title='Snakes', body='Ssssssss')
# py.posts.append(p)
# #commit changes
# db.session.add(py)
# print('POSTS:' + str(py.posts))
#delete everything after use (so duplicates aren't created)