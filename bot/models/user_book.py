import enum
from typing import Tuple
from peewee import ForeignKeyField, CharField, Model, CompositeKey
from . import user as u
from . import book as b

class User_Book_Status(enum.Enum):
    WANT_TO_READ = "want to read"
    READING = "reading"
    READ = "read"
    
class User_Book(Model):
    user = ForeignKeyField(u.User)
    book = ForeignKeyField(b.Book)
    status = CharField(null = False, default=User_Book_Status.WANT_TO_READ.value)
    class Meta:
        primary_key = CompositeKey('user', 'book')
    
def createOrGetUserBook(user: u.User, book: b.Book) -> Tuple[User_Book, bool]:
    return User_Book.get_or_create(user=user, book=book)

def getCurrentReadingTitles(user: u.User)->list[str]:
    query = (b.Book
                .select()
                .join(User_Book)
                .join(u.User)
                .where((u.User.name == user.name) and (User_Book.status == User_Book_Status.READING.value)))
    return [(book.title + " by " + book.author) for book in query]

def getBooksByStatus(user: u.User, status: User_Book_Status) -> list[b.Book]:
    query = (User_Book
            .select(User_Book, b.Book, u.User)
            .where(User_Book.status == status.value)
            .join(b.Book)
            .switch(User_Book)
            .join(u.User)
            .where(u.User.name == user.name))
    return [b.Book.get_by_id(ub.book.id) for ub in query]
        
def getPagesRead(user: u.User) -> int:
    books_read = getBooksByStatus(user, User_Book_Status.READ)
    total_pages = 0
    for book in books_read:
        total_pages += int(str(book.num_pages))   
    return total_pages