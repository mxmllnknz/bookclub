from .test import spinUp, tearDown
from src.models.user import createOrGetUser, User
from peewee import IntegrityError

def testCreateOrGetUserCreate():
    db = spinUp()
    user, created = createOrGetUser("Fred#0")
    assert created == True
    assert user.name == 'Fred#0'
    assert user.formatted_name == 'Fred'
    assert not user.deleted_at
    tearDown(db)

def testCreateOrGetUserGet():
    db = spinUp()
    user, created = createOrGetUser("Fred#0")
    assert created == True
    user, created = createOrGetUser("Fred#0")
    assert created == False
    assert user.name == 'Fred#0'
    assert user.formatted_name == 'Fred'
    assert not user.deleted_at
    tearDown(db)

def testCreateOrGetUserFail():
    db = spinUp()
    _, created = createOrGetUser("Fred#0")
    assert created == True
    try:
        _, created = createOrGetUser("Fred")
    except IntegrityError:
        query = (User.select())
        assert len(query) == 1