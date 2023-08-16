from . import test_setup as t
from models import user_book as ub
from peewee import IntegrityError

def testCreateOrGetUserBookCreate():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    userbook, created = ub.createOrGetUserBook(user=user, book=book)
    assert created == True
    assert userbook.user.name == 'test#0'
    assert userbook.book.title == 'test title'

def testCreateOrGetUserBookGet():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    userbook, created = ub.createOrGetUserBook(user=user, book=book)
    assert created == True
    userbook, created = ub.createOrGetUserBook(user=user, book=book)
    assert created == False
    assert userbook.user.name == 'test#0'
    assert userbook.book.title == 'test title'

def testCreateOrGetUserBookFail():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    _, created = ub.createOrGetUserBook(user=user, book=book)
    assert created == True
    try:
        _, created = ub.createOrGetUserBook(user=user, book=book)
    except IntegrityError:
        query = (ub.User_Book.select())
        assert len(query) == 1
    
def testGetCurrentReadingTitlesNominal():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    t.createTestUserBook(user, book, ub.User_Book_Status.READING)
    assert len(ub.getCurrentReadingTitles(user)) == 1

def testGetCurrentReadingTitlesEmpty():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    t.createTestUserBook(user, book, ub.User_Book_Status.READ)
    assert ub.getCurrentReadingTitles(user) == []

def testGetCurrentReadingTitlesMany():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book1 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id')
    t.createTestUserBook(user, book1, ub.User_Book_Status.READING)
    book2 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id 1')
    t.createTestUserBook(user, book2, ub.User_Book_Status.READING)
    assert len(ub.getCurrentReadingTitles(user)) == 2
    
def testGetBooksByStatus():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book1 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id1')
    t.createTestUserBook(user, book1, ub.User_Book_Status.READING)
    book2 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id2')
    t.createTestUserBook(user, book2, ub.User_Book_Status.READ)
    book3 = t.createTestBook(title='teub.st title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id3')
    t.createTestUserBook(user, book3, ub.User_Book_Status.WANT_TO_READ)
    assert len(ub.getBooksByStatus(user, ub.User_Book_Status.WANT_TO_READ)) == 1
    assert len(ub.getBooksByStatus(user, ub.User_Book_Status.READ)) == 1
    assert len(ub.getBooksByStatus(user, ub.User_Book_Status.READING)) == 1
    
def testGetPagesReadNominal():
    db = t.spinUp()
    user = t.createTestUser('test#0')
    book1 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id1')
    t.createTestUserBook(user, book1, ub.User_Book_Status.READ)
    book2 = t.createTestBook(title='test title', author='test author', year='4242', num_pages='1', publisher='test publisher', api_id='test api id2')
    t.createTestUserBook(user, book2, ub.User_Book_Status.READ)
    assert ub.getPagesRead(user) == 43
    book3 = t.createTestBook(title='teub.st title', author='test author', year='4242', num_pages='42', publisher='test publisher', api_id='test api id3')
    t.createTestUserBook(user, book3, ub.User_Book_Status.READING)
    assert ub.getPagesRead(user) == 43
