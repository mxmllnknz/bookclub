from . import test_setup as t
from models import book as b
from peewee import IntegrityError

def testCreateOrGetBookCreate():
    db = t.spinUp()
    book, created = b.createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    assert book.title == 'test title'
    assert book.author == 'test author'
    assert book.year == 4242
    assert book.num_pages == '42'
    assert book.publisher == 'test publisher'
    assert book.api_id == 'test api id'

def testCreateOrGetBookGet():
    db = t.spinUp()
    book, created = b.createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    book, created = b.createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == False
    assert book.title == 'test title'
    assert book.author == 'test author'
    assert book.year == 4242
    assert book.num_pages == '42'
    assert book.publisher == 'test publisher'
    assert book.api_id == 'test api id'

def testCreateOrGetBookFail():
    db = t.spinUp()
    _, created = b.createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    try:
        _, created = b.createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    except IntegrityError:
        query = (b.Book.select())
        assert len(query) == 2