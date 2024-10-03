from typing import Generator
import pytest
from src.config import DBURL, Session
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.orm.session import Session as OrmSession
from src.main import create_app


@pytest.fixture(scope='function')
def _session() -> Generator[OrmSession]:
    s = Session()
    yield s
    s.close()


@pytest.fixture(scope='module')
def _app() -> FastAPI:
    return create_app()


@pytest.fixture(scope='module')
def _client(_app) -> TestClient:
    cli = TestClient(app=_app, base_url='http://localhost:8000')
    return cli
