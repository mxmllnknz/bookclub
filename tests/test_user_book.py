from .test import spinUp, tearDown, createTestBook, createTestUser, createTestUserBook
from src.models.user_book import createOrGetUserBook, getCurrentReadingTitles, getBooksByStatus, User_Book, User_Book_Status
from src.models.user import User
from src.models.book import Book
from peewee import IntegrityError

def testCreateOrGetUserBookCreate():
    db = spinUp()
    user = createTestUser('test#0')
    book = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    ub, created = createOrGetUserBook(user=user, book=book)
    assert created == True
    assert ub.user.name == 'test#0'
    assert ub.book.title == 'test title'
    tearDown(db)

def testCreateOrGetUserBookGet():
    db = spinUp()
    user = createTestUser('test#0')
    book = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    ub, created = createOrGetUserBook(user=user, book=book)
    assert created == True
    ub, created = createOrGetUserBook(user=user, book=book)
    assert created == False
    assert ub.user.name == 'test#0'
    assert ub.book.title == 'test title'
    tearDown(db)

def testCreateOrGetUserBookFail():
    db = spinUp()
    user = createTestUser('test#0')
    book = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    _, created = createOrGetUserBook(user=user, book=book)
    assert created == True
    try:
        _, created = createOrGetUserBook(user=user, book=book)
    except IntegrityError:
        query = (User_Book.select())
        assert len(query) == 1
    tearDown(db)
    
def testGetCurrentReadingTitlesNominal():
    db = spinUp()
    user = createTestUser('test#0')
    book = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    createTestUserBook(user, book, User_Book_Status.READING)
    assert len(getCurrentReadingTitles(user)) == 1
    tearDown(db)

def testGetCurrentReadingTitlesEmpty():
    db = spinUp()
    user = createTestUser('test#0')
    book = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    createTestUserBook(user, book, User_Book_Status.READ)
    assert getCurrentReadingTitles(user) == []
    tearDown(db)

def testGetCurrentReadingTitlesMany():
    db = spinUp()
    user = createTestUser('test#0')
    book1 = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    createTestUserBook(user, book1, User_Book_Status.READING)
    book2 = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id 1')
    createTestUserBook(user, book2, User_Book_Status.READING)
    assert len(getCurrentReadingTitles(user)) == 2
    tearDown(db)
    
def testGetBooksByStatus():
    db = spinUp()
    user = createTestUser('test#0')
    book1 = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id1')
    createTestUserBook(user, book1, User_Book_Status.READING)
    book2 = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id2')
    createTestUserBook(user, book2, User_Book_Status.READ)
    book3 = createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id3')
    createTestUserBook(user, book3, User_Book_Status.WANT_TO_READ)
    assert len(getBooksByStatus(user, User_Book_Status.WANT_TO_READ)) == 1
    assert len(getBooksByStatus(user, User_Book_Status.READ)) == 1
    assert len(getBooksByStatus(user, User_Book_Status.READING)) == 1