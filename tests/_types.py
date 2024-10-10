from typing import Annotated, Generic, TypeVar
import pytest

_T = TypeVar("_T")
Fixture = Annotated[_T, pytest.fixture]