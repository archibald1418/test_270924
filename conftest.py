from typing import Generator

import pytest

from src.models import BaseModel
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.orm.session import Session as OrmSession
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import create_app

from tests._types import Fixture

TEST_DBURL = 'postgresql+pg8000://test@localhost:5432/test'

@pytest.fixture(scope='session')
def _db() -> Generator[sessionmaker]:
    engine = create_engine(TEST_DBURL)
    BaseModel.metadata.create_all(bind=engine)
    yield sessionmaker(engine)
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def _session(_db: Fixture[sessionmaker]) -> Generator[OrmSession]:
    Session: OrmSession = _db()
    yield Session
    Session.close()


@pytest.fixture(scope='module', autouse=True)
def _app() -> FastAPI:
    return create_app()


@pytest.fixture(scope='module')
def _client(_app: Fixture[FastAPI]) -> TestClient:
    cli = TestClient(app=_app, base_url='http://localhost:8000')
    return cli
