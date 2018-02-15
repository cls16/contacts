import re

from marshmallow import Schema, fields, validates, ValidationError, pre_load


alpha_re = re.compile(r'^[a-zA-Z]+$')
phonenumber_re = re.compile(r'\d{3}-\d{3}-\d{4}')

class BaseSchema(Schema):
    @pre_load
    def preload_cleanup(self, data):
        retval = {}
        # strip whitespace
        for key, val in data.items():
            retval[key] = val.strip() or None
            
        return retval

class ContactSchema(BaseSchema):
    firstname = fields.Str()
    lastname = fields.Str()
    email = fields.Email()
    phonenumber = fields.Str()

    @validates('firstname')
    def validate_firstname(self, firstname):
        firstname = firstname.strip()
        if not alpha_re.match(firstname):
            raise ValidationError('First name invalid. No numbers or special characters allowed.')
        else:
            return firstname

    @validates('lastname')
    def validate_lastname(self, lastname):
        lastname = lastname.strip()
        if not alpha_re.match(lastname):
            raise ValidationError('Last name invalid. No numbers or special characters allowed.')

    @validates('phonenumber')
    def validate_phonenumber(self, phonenumber):
        phonenumber = phonenumber.strip()
        if not phonenumber_re.match(phonenumber):
            raise ValidationError('You must have a dash between each group of numbers.')

error_messages = {'null': 'Please fill out this field.'}

class UserSchema(BaseSchema):
    username = fields.Str(required=True, allow_none=False, error_messages=error_messages)
    password = fields.Str(required=True, allow_none=False, error_messages=error_messages)

    







