import pytest
import shutil
from flask import Flask
from flask.testing import FlaskClient
from tempfile import mkdtemp


@pytest.fixture
def app(minio_mock: None) -> Flask:
    from app import create_app, config

    config.TESTING = True
    config.DATA_DIRECTORY = mkdtemp(prefix="CHIMP_TESTING_")
    app = create_app(config)

    ctx = app.app_context()
    ctx.push()

    yield app

    shutil.rmtree(config.DATA_DIRECTORY)
    ctx.pop()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
