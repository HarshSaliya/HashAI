import pytest

from app.embedder import Embedder
from app.llm import Llm


@pytest.fixture(scope="session")
def embedder():
    return Embedder()


@pytest.fixture(scope="session")
def llm():
    return Llm()
