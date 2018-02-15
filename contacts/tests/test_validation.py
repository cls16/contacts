import contacts.validation as val 

class TestContactSchema:
    def test_firstname_valid(self):
        data = {'firstname': 'John'}
        result = val.ContactSchema().load(data)

        assert not result.errors
        assert result.data['firstname'] == 'John'

    def test_firstname_invalid(self):
        data = {'firstname': 'f00'}
        result = val.ContactSchema().load(data)

        assert result.errors == {'firstname': ['First name invalid. No numbers or special characters allowed.']}
   
    def test_whitespace_trimmed(self):
        data = {'firstname':'John ', 'lastname':' Doe', 'email':' jd@space.org ',
         'phonenumber':' 000-000-0000 '}
        result = val.ContactSchema().load(data)
        
        assert not result.errors

    def test_lastname_valid(self):
        data = {'lastname': 'John'}
        result = val.ContactSchema().load(data)

        assert not result.errors
        assert result.data['lastname'] == 'John'

    def test_lastname_invalid(self):
        data = {'lastname': 'f00'}
        result = val.ContactSchema().load(data)

        assert result.errors == {'lastname': ['Last name invalid. No numbers or special characters allowed.']}

    def test_email_valid(self):
        data = {'email': 'johndoe@gmail.com'}
        result = val.ContactSchema().load(data)

        assert not result.errors
        assert result.data['email'] == 'johndoe@gmail.com'

    def test_email_invalid(self):
        data = {'email': 'foo'}
        result = val.ContactSchema().load(data)

        assert result.errors == {'email': ['Not a valid email address.']}

    def test_phonenumber_valid(self):
        data = {'phonenumber': '111-111-1111'}
        result = val.ContactSchema().load(data)

        assert not result.errors
        assert result.data['phonenumber'] == '111-111-1111'

    def test_phonenumber_invalid(self):
        data = {'phonenumber': 'foo'}
        result = val.ContactSchema().load(data)

        assert result.errors == {'phonenumber': ['You must have a dash between each group of numbers.']}


class TestUserSchema:
    def test_insert_user(self):
        data = {'username': 'randomUser', 'password': 'randomPass'}
        result = val.UserSchema().load(data)

        assert not result.errors

    def test_username_required(self):
        data = {'username': '', 'password': 'randomPass'}
        result = val.UserSchema().load(data)

        assert result.errors == {'username': ['Please fill out this field.']}

    def test_password_required(self):
        data = {'username': 'randomUser', 'password': ''}
        result = val.UserSchema().load(data)

        assert result.errors == {'password': ['Please fill out this field.']}

