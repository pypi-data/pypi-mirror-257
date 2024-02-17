import datetime

import data

import meritous.properties

def test_date_property():
    p = meritous.properties.DateProperty()
    assert p.type == datetime.date
    assert p.validate(datetime.date.fromisoformat('2023-01-10')) == True

def test_date_default():
    p = meritous.properties.DateProperty(default=datetime.date.fromisoformat('2023-01-10'))
    assert p.default == datetime.date.fromisoformat('2023-01-10')

def test_date_required():
    p = meritous.properties.DateProperty(required=True)
    assert p.is_required == True