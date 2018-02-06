import flask_webtest
from contacts.app import app, db, Contact


class TestWeb:
    @classmethod
    def setup_class(self):
        self.app = app
        self.app.testing = True
        self.client = flask_webtest.TestApp(self.app, db=db, use_session_scopes=True)

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
    

       
        
        