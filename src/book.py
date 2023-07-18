import db
from typing import Optional
class Book:
    def __init__(self, title, num_pages, author, year, publisher="", api_id=""):
        self.id = 0
        self.title = title
        self.num_pages = num_pages
        self.author = author
        self.publisher = publisher
        self.year = year
        self.api_id = api_id
    
        cursor = db.get_cursor()
        
        # Add a new row or get the existing row and initialize a Book obj
        cursor.execute(f"INSERT OR IGNORE INTO books (title, author, page_count, publisher, published_year, api_id) \
                        VALUES ('{self.title}', '{self.author}', {self.num_pages}, '{self.publisher}', '{self.year}', '{self.api_id}')")
        cursor.execute(f"SELECT * FROM books WHERE title = '{self.title}' AND author = '{self.author}' AND publisher = '{self.publisher}' \
                        AND page_count = {self.num_pages} AND published_year = '{self.year}' AND api_id = '{self.api_id}'")
        res = cursor.fetchone()
        self.id = res[0]
        cursor.connection.commit()
        cursor.connection.close()
        
    def __repr__(self) -> str:
        return f'{self.title} by {self.author}, published in {self.year} by {self.publisher}, {self.num_pages} pages'
    
def getBookById(id: int) -> Optional[Book]:
    cursor = db.get_cursor()
    cursor.execute(f"SELECT * FROM books WHERE \
                        id = {id}")
    book = cursor.fetchone()
    cursor.connection.close()
    return Book(book[2], book[4], book[3], book[6], publisher=book[5], api_id=book[7])