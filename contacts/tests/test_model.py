from contacts.app import db
from contacts import model


def test_connection():
    result = db.engine.execute("select 1=0")
    assert result.scalar() == 0


def test_contacts_create():
    if 'contacts' in model.sqlite_table_names():
        model.contacts_drop()

    model.contacts_create()

    assert 'contacts' in model.sqlite_table_names()


def test_contact_insert():
    assert model.contacts_count() == 0

    model.contacts_insert('person', 'person@gmail.com')

    assert model.contacts_count() == 1

def test_html_change()
    assert
