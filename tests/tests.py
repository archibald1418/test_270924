import pytest
from fastapi.responses import JSONResponse

from src.models import Product

from ._types import Fixture
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session as OrmSession
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine

from src.dto import ProductDto

from http import HTTPStatus


def test_root(_client: TestClient):
    res = _client.get("/")
    assert res.status_code == HTTPStatus.OK
    assert res.json() == { "Hello": "This is App" }



def test_add_one(_session: OrmSession, _random_product: Product):
    print(_random_product)
    _session.add(_random_product)
    _session.commit()
    stmt = select(Product).limit(1)
    row = _session.execute(stmt).fetchone()
    assert row[0] == _random_product

def test_get(_session): ...

    
# @pytest.mark.parametrize(
#     'product'
# )
# def test_new_products(
#     _dbsession: Fixture[OrmSession],
#     product):
#     ...
