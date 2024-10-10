import pytest
from fastapi.responses import JSONResponse

from ._types import Fixture
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.orm.session import Session as OrmSession

from http import HTTPStatus


def test_root(_client: TestClient):
    res = _client.get("/")
    assert res.status_code == HTTPStatus.OK
    assert res.json() == { "Hello": "This is App" }
    
    
# @pytest.mark.parametrize(
#     'product'
# )
# def test_new_products(
#     _dbsession: Fixture[OrmSession],
#     product):
#     ...
