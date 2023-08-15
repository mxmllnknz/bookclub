import enum
from typing import Tuple
from peewee import ForeignKeyField, CharField
from models.user import User
from models.book import Book
from database import BaseModel
class User_Book_Status(enum.Enum):
    WANT_TO_READ = "want to read"
    READING = "reading"
    READ = "read"
    
class User_Book(BaseModel):
    user = ForeignKeyField(User)
    book = ForeignKeyField(Book)
    status = CharField(null = False, default=User_Book_Status.WANT_TO_READ.value)
    
def createOrGetUserBook(user: User, book: Book) -> Tuple[User_Book, bool]:
    return User_Book.get_or_create(user=user, book=book)

def getCurrentReadingTitles(user: User)->list[str]:
    query = (Book
                .select()
                .join(User_Book)
                .join(User)
                .where((User.name == user.name) and (User_Book.status == User_Book_Status.READING.value)))
    reading = []
    for book in query:
        reading.append(book.title + " by " + book.author)
    return reading

def getBooksByStatus(user: User, status: User_Book_Status) -> list[Book]:
    query = (User_Book
            .select(User_Book, Book, User)
            .where(User_Book.status == status)
            .join(Book)
            .join(User)
            .where(User.name == user.name))
    res = []
    for ub in query:
        res.append(Book.get_by_id(ub.book.id))
    return res
        