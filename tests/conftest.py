import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.embedder import Embedder
from app.llm import Llm


@pytest.fixture(scope="session")
def embedder():
    return Embedder()


@pytest.fixture(scope="session")
def llm():
    return Llm()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
