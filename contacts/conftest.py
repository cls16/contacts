import os


def pytest_configure(config):
    os.environ['DB_CONN'] = 'sqlite:///'