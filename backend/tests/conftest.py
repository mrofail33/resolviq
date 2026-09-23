import os
import tempfile

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["AI_PROVIDER"] = "mock"
os.environ["UPLOAD_DIR"] = tempfile.mkdtemp()

import pytest
from fastapi.testclient import TestClient

from app.db.session import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)
