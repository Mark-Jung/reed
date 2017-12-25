from app import create_app
from db import db as _db
import pytest

TESTDB = 'test.db'
TESTDB_PATH = "/reed/project/data/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH

@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


