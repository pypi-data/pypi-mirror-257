

import pytest

import test_data as data

from meritous import Model, Schema
from meritous.core import Property
import meritous.exceptions

class ModelTest(Model):
    _schema = {
        data.TEST_STR : Property(str, data.TEST_STR_ALT)
    }

def test_model_init():
    m = ModelTest()
    assert isinstance(m._schema, Schema)
    assert m.TEST == data.TEST_STR_ALT
    m.TEST = data.TEST_STR
    assert m.TEST == data.TEST_STR
    m = ModelTest(_schema={
        data.TEST_STR : Property(int, data.TEST_INT)
    })
    assert isinstance(m._schema, Schema)
    assert m.TEST == data.TEST_INT

def test_model_init_invalid_schema():
    with pytest.raises(meritous.exceptions.ModelException):
        m = ModelTest(_schema=1)

def test_model_invalid_setattr():
    m = ModelTest()
    with pytest.raises(meritous.exceptions.PropertyException):
        m.TEST = data.TEST_INT


def test_model_marshall():
    class MockStore:
        def marshall(self, value, property):
            return value + data.TEST_STR
    m = ModelTest()
    assert m.TEST == data.TEST_STR_ALT
    d = m.marshall(MockStore())
    assert type(d) == dict
    assert d[data.TEST_STR] == data.TEST_STR_ALT + data.TEST_STR
