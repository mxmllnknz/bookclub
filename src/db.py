import sqlite3
import user

def get_cursor(db_name='club.db') -> sqlite3.Cursor:
    conn = sqlite3.connect(db_name)
    return conn.cursor()

def init_db():
    conn = sqlite3.connect('club.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users ( \
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    name TEXT NOT NULL UNIQUE, \
                    formatted_name TEXT NOT NULL UNIQUE)")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS books ( \
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    title TEXT NOT NULL, \
                    author TEXT NOT NULL, \
                    page_count INT NOT NULL, \
                    publisher TEXT, \
                    published_year TEXT NOT NULL, \
                    api_id TEXT) \
                    ")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS user_books ( \
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    user_id INTEGER, \
                    book_id INTEGER, \
                    read BOOLEAN DEFAULT false, \
                    reading BOOLEAN DEFAULT false, \
                    FOREIGN KEY(user_id) REFERENCES users(id), \
                    FOREIGN KEY(book_id) REFERENCES books(id)) \
                    ")

    conn.commit()
    conn.close()