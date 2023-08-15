from peewee import SqliteDatabase
from typing import Union
from src.models import User, Book, User_Book, User_Book_Status
from src.database import get_db

MODELS = [User, Book, User_Book]

def spinUp():
    return get_db(':memory:')

def tearDown(db: SqliteDatabase):
    db.drop_tables(MODELS)
    
def createTestUser(name: str) -> User:
    return User.create(name = name, formatted_name=name[:-2])

def createTestBook(title: str, author: str, year: str, num_pages: str, publisher: str, api_id: str) -> Book:
    return Book.create(title=title, author=author, year=int(year), num_pages=num_pages, publisher=publisher, api_id=api_id)

def createTestUserBook(user: User, book: Book, status: User_Book_Status) -> User_Book:
    return User_Book.create(user=user, book=book, status=status.value)