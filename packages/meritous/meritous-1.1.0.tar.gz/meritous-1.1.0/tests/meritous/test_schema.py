

import pytest

import test_data as data

from meritous import Schema
from meritous.core import Property
import meritous.exceptions

def test_schema_init():
    s = Schema(**{})


def test_schema_invalid_property():
    with pytest.raises(meritous.exceptions.SchemaException):
        s = Schema(**{ data.TEST_STR : data.TEST_INT })


def test_schema_add_name():
     s = Schema({
          data.TEST_STR : Property(str)
     })
     assert s[data.TEST_STR].name == data.TEST_STR

