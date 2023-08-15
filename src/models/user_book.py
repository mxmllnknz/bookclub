import enum
from typing import Tuple
from peewee import ForeignKeyField, CharField, Model, CompositeKey
from .user import User
from .book import Book
class User_Book_Status(enum.Enum):
    WANT_TO_READ = "want to read"
    READING = "reading"
    READ = "read"
    
class User_Book(Model):
    user = ForeignKeyField(User)
    book = ForeignKeyField(Book)
    status = CharField(null = False, default=User_Book_Status.WANT_TO_READ.value)
    class Meta:
        primary_key = CompositeKey('user', 'book')
    
def createOrGetUserBook(user: User, book: Book) -> Tuple[User_Book, bool]:
    return User_Book.get_or_create(user=user, book=book)

def getCurrentReadingTitles(user: User)->list[str]:
    query = (Book
                .select()
                .join(User_Book)
                .join(User)
                .where((User.name == user.name) and (User_Book.status == User_Book_Status.READING.value)))
    return [(book.title + " by " + book.author) for book in query]

def getBooksByStatus(user: User, status: User_Book_Status) -> list[Book]:
    query = (User_Book
            .select(User_Book, Book, User)
            .where(User_Book.status == status.value)
            .join(Book)
            .switch(User_Book)
            .join(User)
            .where(User.name == user.name))
    return [Book.get_by_id(ub.book.id) for ub in query]
        