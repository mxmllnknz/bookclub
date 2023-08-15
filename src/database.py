from peewee import SqliteDatabase, Model
from .models import User, Book, User_Book

MODELS = [User, Book, User_Book]

def get_db(db_name='club.db') -> SqliteDatabase:
  db = SqliteDatabase(f'{db_name}')
  db.bind(MODELS, bind_refs=False, bind_backrefs=False)
  db.connect()
  db.create_tables(MODELS)
  return db