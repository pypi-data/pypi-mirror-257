import pytest

import data

import meritous.properties
import meritous.exceptions

def test_str_property():
    p = meritous.properties.StrProperty()
    assert p.type == str
    assert p.validate(data.TEST_STR) == True

def test_str_default():
    p = meritous.properties.StrProperty(default=data.TEST_STR)
    assert p.default == data.TEST_STR

def test_str_required():
    p = meritous.properties.StrProperty(required=True)
    assert p.is_required == True