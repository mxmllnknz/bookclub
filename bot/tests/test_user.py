from . import test_setup as t
from models import user as u
from peewee import IntegrityError

def testCreateOrGetUserCreate():
    db = t.spinUp()
    user, created = u.createOrGetUser("Fred#0")
    assert created == True
    assert user.name == 'Fred#0'
    assert user.formatted_name == 'Fred'
    assert not user.deleted_at

def testCreateOrGetUserGet():
    db = t.spinUp()
    user, created = u.createOrGetUser("Fred#0")
    assert created == True
    user, created = u.createOrGetUser("Fred#0")
    assert created == False
    assert user.name == 'Fred#0'
    assert user.formatted_name == 'Fred'
    assert not user.deleted_at

def testCreateOrGetUserFail():
    db = t.spinUp()
    _, created = u.createOrGetUser("Fred#0")
    assert created == True
    try:
        _, created = u.createOrGetUser("Fred")
    except IntegrityError:
        query = (u.User.select())
        assert len(query) == 1