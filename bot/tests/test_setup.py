from peewee import SqliteDatabase
from models import user as u
from models import book as b
from models import user_book as ub
from database import util as database

MODELS = [u.User, b.Book, ub.User_Book]

def spinUp():
    return database.get_db(':memory:')

def tearDown(db: SqliteDatabase):
    db.drop_tables(MODELS)
    
def createTestUser(name: str) -> u.User:
    return u.User.create(name = name, formatted_name=name[:-2])

def createTestBook(title: str, author: str, year: str, num_pages: str, publisher: str, api_id: str) -> b.Book:
    return b.Book.create(title=title, author=author, year=int(year), num_pages=num_pages, publisher=publisher, api_id=api_id)

def createTestUserBook(user: u.User, book: b.Book, status: ub.User_Book_Status) -> ub.User_Book:
    return ub.User_Book.create(user=user, book=book, status=status.value)