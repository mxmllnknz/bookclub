import db
from book import Book, getBookById
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
        
    def getUserReadingTitles(self) -> list[Book]:
        cursor = db.get_cursor()
        cursor.execute(f"SELECT * FROM user_books where \
                        user_id = {self.id} AND reading = true")
        books = cursor.fetchall()
        reading = []
        for bookTup in books:
            book = getBookById(bookTup[0])
            if book:
                reading.append(book)
        return reading
    