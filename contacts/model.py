from contacts.app import db


def contacts_create():
    sql = """
        create table contacts(
            id integer primary key autoincrement,
            first_name varchar(255),
            email_address varchar(255)
        )
    """
    db.engine.execute(sql)


def sqlite_table_names():
    sql = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """
    rows = db.engine.execute(sql)
    return [row[0] for row in rows]


def contacts_drop():
    sql = "drop table contacts"
    db.engine.execute(sql)


def contacts_count():
    sql = "select count(id) from contacts"
    result = db.engine.execute(sql)
    return result.scalar()


def contacts_insert(first_name, email):
    sql = "insert into contacts(first_name, email_address) values('{}','{}')"\
           .format(first_name, email)
    db.engine.execute(sql)
