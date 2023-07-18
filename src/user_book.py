import enum
import db

class User_Book_Status(enum.Enum):
    WANT_TO_READ = "want to read"
    READING = "reading"
    READ = "read"
    
class User_Book():
    def __init__(self, user_id: int, book_id: int):
        self.id = 0
        self.user_id = user_id
        self.book_id = book_id
        self.status = "want to read"
        
        cursor = db.get_cursor()
        
        # Add a new row or get the existing row and initialize a User obj
        cursor.execute(f"INSERT OR IGNORE INTO user_books (user_id, book_id, status) \
                        VALUES ({self.user_id}, {self.book_id}, '{self.status}')")
        cursor.execute(f"SELECT * FROM user_books WHERE user_id = {self.user_id} AND book_id = {self.book_id}")
        res = cursor.fetchone()
        self.id = res[0]
        cursor.connection.commit()
        cursor.connection.close()
        
    def update(self, status: User_Book_Status):
        cursor = db.get_cursor()
        self.status = status
        cursor.execute(f"UPDATE user_books SET \
                            status = '{self.status}' \
                            WHERE user_id = {self.user_id} AND \
                            book_id = {self.book_id}")
        cursor.connection.commit()
        cursor.connection.close()