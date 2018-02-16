import flask_webtest
from contacts.app import app, db, Contact, User
import flask_login

class TestWeb:
    @classmethod
    def setup_class(self):
        self.app = app
        self.app.testing = True
        self.unauth_client = flask_webtest.TestApp(self.app, db=db, use_session_scopes=True)
        self.client = flask_webtest.TestApp(self.app, db=db, use_session_scopes=True)
        self.user = user = User.testing_create()
        self.client.post('/login', params={'username':user.username,
         'password':user.password}, status=302)

    def setup(self):
        Contact.query.delete()
        db.session.commit()

    def test_form_success(self):
        resp = self.client.get('/addcontact')

        form = resp.form
        form['firstname'] = 'john'
        form['lastname'] = 'doe'
        form['email'] = 'johndoe@something.org'
        form['phonenumber'] = '000-000-0000'
        resp = form.submit()

        resp = resp.follow()
        assert resp.request.url == 'http://localhost/contacts'
        
        contact = Contact.query.one()
        assert contact.firstname == 'john'
        assert contact.lastname == 'doe'
        assert contact.email == 'johndoe@something.org'
        assert contact.phonenumber == '000-000-0000'

    def test_form_fields_ivalid(self):
        resp = self.client.get('/addcontact')

        form = resp.form
        form['firstname'] = 'joh3*'
        form['lastname'] = 'do3#'
        form['email'] = 'johndoesomethingorg'
        form['phonenumber'] = '000-000&0000'
        resp = form.submit()

        error_p = resp.pyquery('p.error')
        assert error_p.eq(0).text() == 'First name invalid. No numbers or special characters allowed.'
        assert error_p.eq(1).text() == 'Last name invalid. No numbers or special characters allowed.' 
        assert error_p.eq(2).text() == 'Not a valid email address.' 
        assert error_p.eq(3).text() == 'You must have a dash between each group of numbers.' 
        
        inputs = resp.pyquery('input')
        assert inputs.eq(0).val() == 'joh3*'
        assert inputs.eq(1).val() == 'do3#'
        assert inputs.eq(2).val() == 'johndoesomethingorg'
        assert inputs.eq(3).val() == '000-000&0000'
        assert Contact.query.count() == 0       

    def test_contacts(self):
        #add contact to database
        newcontact = Contact(firstname = 'john', lastname = 'doe', 
        email = 'johndoe@something.org', phonenumber = '000-000-0000')
        db.session.add(newcontact)
        db.session.commit()
        
        resp = self.client.get('/contacts')
        doc = resp.pyquery
        
        trs = doc('tr')
        assert len(trs) == 2
        
        #test header row
        header_tr = trs.eq(0)
        header_th = header_tr.find('th')
        assert header_th.eq(0).text() == ''
        assert header_th.eq(1).text() == 'First Name'
        assert header_th.eq(2).text() == 'Last Name'
        assert header_th.eq(3).text() == 'Email'
        assert header_th.eq(4).text() == 'Phone #'

        #test contact row
        contact_tr = trs.eq(1)
        contact_td = contact_tr.find('td')
        input = contact_td.eq(0).find('input')
        assert input.attr('type') == 'checkbox'
        assert input.attr('name') == 'contact_id'
        assert input.val() == str(newcontact.id)
        assert contact_td.eq(1).text() == 'john'
        assert contact_td.eq(2).text() == 'doe'
        assert contact_td.eq(3).text() == 'johndoe@something.org'
        assert contact_td.eq(4).text() == '000-000-0000'
        
    def test_delete_contact(self):
        #add contact to database
        newcontact = Contact(firstname = 'john', lastname = 'doe', 
        email = 'johndoe@something.org', phonenumber = '000-000-0000')
        db.session.add(newcontact)
        db.session.commit()

        resp = self.client.get('/contacts')
        doc = resp.pyquery

        #define number of table rows in contacts table as variable
        contact_trs = len(Contact.query.all())
    
        #delete contact
        Contact.query.filter_by(id=1).delete()
        db.session.commit()

        #make sure one less contact in table
        current_contact_trs = contact_trs - 1
        assert len(Contact.query.all()) == current_contact_trs

        #refresh page
        resp = self.client.get('/contacts')
        #make sure no contacts displayed
        resp.mustcontain('No contacts to show')

    def test_login(self):
        resp = self.client.get('/login')

        form = resp.form
        form['username'] = self.user.username
        form['password'] = self.user.password
        resp = form.submit()

        resp = resp.follow()
        print(resp)
        assert resp.request.url == 'http://localhost/home'
        assert 'Hi, ' + self.user.username in resp

    def test_username_required(self):
        resp = self.client.get('/login')

        form = resp.form
        form['username'] = ''
        form['password'] = self.user.password
        resp = form.submit()

        assert 'Please fill out this field.' in resp
        
    def test_password_required(self):
        resp = self.client.get('/login')

        form = resp.form
        form['username'] = self.user.username
        form['password'] = ''
        resp = form.submit()

        assert 'Please fill out this field.' in resp

    def test_login_invalid(self):
        resp = self.client.get('/login')

        form = resp.form
        form['username'] = 'invalidusername'
        form['password'] = 'invalidpassword'
        resp = form.submit()

        assert 'username and password not valid' in resp

    def test_addcontact_login_required(self):
        self.unauth_client.get('/addcontact', status=401)

    def test_contacts_login_required(self):
        self.unauth_client.get('/contacts', status=401)
        
    def test_logout(self):
        logout_client = flask_webtest.TestApp(app, db=db, use_session_scopes=True)
        logout_user = User.testing_create()
        logout_client.post('/login', params={'username':logout_user.username,
         'password':logout_user.password}, status=302)
        
        resp = logout_client.get('/logout')

        resp = logout_client.get('/logout', status=401)

    def test_sign_up(self):
        resp = self.unauth_client.get('/signup')

        form = resp.form
        form['username'] = 'newusername'
        form['password'] = 'newpassword'
        resp = form.submit()


    #def test_saved_contact(self):
    
    

       
        
        