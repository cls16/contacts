import os


def pytest_configure(config):
    os.environ['DB_CONN'] = 'sqlite:///'
    os.environ['TESTING_DB_INIT'] = 'yes'