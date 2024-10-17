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
from src.config import get_engine
from src.dto import ProductDto
from src.models import Product

import faker
import random


from tests._types import Fixture

TEST_DBURL = 'postgresql+pg8000://user@localhost:5432/test'

def _get_engine_override() -> Engine:
    return create_engine(TEST_DBURL)


@pytest.fixture(scope='session')
def _db() -> Generator[sessionmaker, None, None]:
    engine = create_engine(TEST_DBURL)
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    yield sessionmaker(engine)


@pytest.fixture(scope='function')
def _session(_db: Fixture[sessionmaker]) -> Generator[OrmSession, None, None]:
    Session: OrmSession = _db()
    yield Session
    Session.close()


@pytest.fixture(scope='session', autouse=True)
def _app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_engine] = _get_engine_override
    return app


@pytest.fixture(scope='session')
def _client(_app: Fixture[FastAPI]) -> TestClient:
    cli = TestClient(app=_app, base_url='http://localhost:8000')
    return cli


@pytest.fixture(scope='session')
def _faker():
    return faker.Faker()

@pytest.fixture(scope='function')
def _random_product(_faker: faker.Faker) -> Product:
    dto = ProductDto(
        name=_faker.name_female(),
        price=float(
            _faker.random_number(digits=3, fix_len=True)\
            + round(random.random(), 2)
        )
    )
    return Product(**dto.model_dump())

# @pyetst