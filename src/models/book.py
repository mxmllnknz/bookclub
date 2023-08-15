from typing import Tuple
from database import BaseModel
from peewee import DateTimeField, CharField, IntegerField
import datetime

class Book(BaseModel):
    created_at = DateTimeField(null=False, default=datetime.datetime.now())
    updated_at = DateTimeField(null=False, default=datetime.datetime.now())
    deleted_at = DateTimeField(null=True)
    title = CharField(null=False)
    num_pages = CharField(null=False)
    author = CharField(null=False)
    year = IntegerField(null=False)
    api_id = CharField(null=True)
    publisher = CharField(null=True)
        
    def __repr__(self) -> str:
        return f'{self.title} by {self.author}, published in {self.year} by {self.publisher}, {self.num_pages} pages'
    
def createOrGetBook(title: str, author: str, year: str, num_pages: str, **kwargs) -> Tuple[Book, bool]:
    api_id = kwargs.get('api_id', '')
    publisher = kwargs.get('publisher', '')
    return Book.get_or_create(
        title = title, 
        author = author,
        year = year,
        num_pages = num_pages,
        api_id = api_id,
        publisher = publisher
        )