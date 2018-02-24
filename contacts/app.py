from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import contacts.validation as val
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#flask-login
login_manager = LoginManager()
login_manager.init_app(app)

from contacts.model import Contact, User

db.drop_all()
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/addcontact', methods=['GET', 'POST'])
@login_required
def addcontact():
    if request.method == 'POST':
        result = val.ContactSchema().load(request.form)
        if result.errors:
            return render_template('form.html', error_messages=result.errors, 
            values=request.form)
        else:
            form_firstname=request.form['firstname']
            newcontact = Contact(firstname=form_firstname, lastname=request.form['lastname'], 
            email=request.form['email'], phonenumber=request.form['phonenumber'])
            db.session.add(newcontact)
            db.session.commit()
            return redirect(url_for('contacts'))
    elif request.method == 'GET':
        return render_template('form.html', values = {}, 
        message='Please enter your contact information below.')

@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    if request.method == 'POST':
        ids = request.form.getlist('contact_id')
        Contact.query.filter(Contact.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return redirect(url_for('contacts'))
    elif request.method == 'GET':
        return render_template('contacts.html', contacts=Contact.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = val.UserSchema().load(request.form)
        if result.errors:
            form_username = request.form['username']
            return render_template('login.html', error_messages=result.errors, 
            values={})
        
        user = User.validate(request.form['username'], request.form['password'])
        if user is None:
            return render_template('login.html', message='username and password not valid',
            values=request.form) 
        
        session['logged_in'] = True
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        next = request.args.get('next')
        # is_safe_url must be defined and it should check if the url is safe for redirects.
        # if not is_safe_url(next):
        #     return abort(400)

        return redirect(next or url_for('home'))
            
    elif request.method == 'GET':
        return render_template('login.html', values = {}, 
        message='Please login below.')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        result = val.UserSchema().load(request.form)
        if result.errors:
            return render_template('signup.html', error_messages=result.errors, 
            values=request.form)
        else:
            form_username=request.form['username']
            newuser = User(username=form_username, password=request.form['password'])
            db.session.add(newuser)
            db.session.commit()
            user = User.validate(request.form['username'], request.form['password'])
            login_user(user)
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', values = {})

@app.errorhandler(401)
def unauthorized(e):
    return render_template('unauthorized.html'), 401

app.secret_key = 'Uh2}(om`~bn%C57&xQ/h8|/\+dPdCIzDW){'