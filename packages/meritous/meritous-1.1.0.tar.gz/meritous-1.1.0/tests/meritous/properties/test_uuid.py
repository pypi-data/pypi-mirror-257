import pytest
import uuid

import meritous.properties
import meritous.exceptions

def test_uuid_generation():
    p = meritous.properties.UUID4Property()
    assert p.type == str
    uuid.UUID(p.default, version=4)

def test_uuid_failed_validation():
    p = meritous.properties.UUID4Property()
    assert p.validate('1234') == False
    assert p.validate(1234) == False