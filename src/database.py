from peewee import SqliteDatabase, Model

def get_db(db_name='club.db') -> SqliteDatabase:
  return SqliteDatabase(f'{db_name}')

class BaseModel(Model):
  class Meta:
    database = get_db()

    # cursor.execute("CREATE TABLE IF NOT EXISTS users ( \
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT, \
    #                 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
    #                 name TEXT NOT NULL UNIQUE, \
    #                 formatted_name TEXT NOT NULL UNIQUE)")
    
    # cursor.execute("CREATE TABLE IF NOT EXISTS books ( \
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT, \
    #                 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
    #                 title TEXT NOT NULL, \
    #                 author TEXT NOT NULL, \
    #                 page_count INT NOT NULL, \
    #                 publisher TEXT, \
    #                 published_year TEXT NOT NULL, \
    #                 api_id TEXT) \
    #                 ")
    
    # cursor.execute("CREATE TABLE IF NOT EXISTS user_books ( \
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT, \
    #                 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
    #                 user_id INTEGER, \
    #                 book_id INTEGER, \
    #                 status TEXT NOT NULL, \
    #                 FOREIGN KEY(user_id) REFERENCES users(id), \
    #                 FOREIGN KEY(book_id) REFERENCES books(id), \
    #                 UNIQUE(user_id, book_id) ON CONFLICT IGNORE) \
    #                 ")

    # conn.commit()
    # conn.close()