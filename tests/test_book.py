from .test import spinUp, tearDown
from src.models.book import createOrGetBook, Book
from peewee import IntegrityError

def testCreateOrGetBookCreate():
    db = spinUp()
    book, created = createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    assert book.title == 'test title'
    assert book.author == 'test author'
    assert book.year == 4242
    assert book.num_pages == '42'
    assert book.publisher == 'test publisher'
    assert book.api_id == 'test api id'
    tearDown(db)

def testCreateOrGetBookGet():
    db = spinUp()
    book, created = createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    book, created = createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == False
    assert book.title == 'test title'
    assert book.author == 'test author'
    assert book.year == 4242
    assert book.num_pages == '42'
    assert book.publisher == 'test publisher'
    assert book.api_id == 'test api id'
    tearDown(db)

def testCreateOrGetBookFail():
    db = spinUp()
    _, created = createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    assert created == True
    try:
        _, created = createOrGetBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    except IntegrityError:
        query = (Book.select())
        assert len(query) == 2
    tearDown(db)