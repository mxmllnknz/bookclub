import db
from book import Book, getBookById
from user_book import User_Book_Status
class User:
    def __init__(self, name: str):
        self.id = 0
        self.created = None
        self.name = name
        self.formatted_name = str(self.name).split('#')[0]
        self.reading_list = []
        self.read_list = []
        
        cursor = db.get_cursor()
        
        # Add a new row or get the existing row and initialize a User obj
        cursor.execute(f"INSERT OR IGNORE INTO users (name, formatted_name) \
                        VALUES ('{self.name}', '{self.formatted_name}')")
        cursor.execute(f"SELECT * FROM users WHERE name = '{self.name}'")
        res = cursor.fetchone()
        self.id = res[0]
        self.created = res[1]
        cursor.connection.commit()
        cursor.connection.close()
        
    def getUserReadingTitles(self) -> list[str]:
        cursor = db.get_cursor()
        cursor.execute(f"SELECT * FROM user_books WHERE \
                        user_id = {self.id} AND status = '{User_Book_Status.READING.value}'")
        books = cursor.fetchall()
        reading = []
        for bookTup in books:
            book = getBookById(bookTup[3])
            if book:
                reading.append(book.title + " by " + book.author)
        return reading
    