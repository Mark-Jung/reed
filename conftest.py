from app import app
import pytest

@pytest.fixture
def app():
    app = create_app()
    return app

