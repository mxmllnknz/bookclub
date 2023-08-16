from peewee import SqliteDatabase
from models import user as u
from models import book as b
from models import user_book as ub


MODELS = [u.User, b.Book, ub.User_Book]

def get_db(db_name='club.db') -> SqliteDatabase:
  db = SqliteDatabase(f'{db_name}')
  db.bind(MODELS, bind_refs=False, bind_backrefs=False)
  db.connect()
  db.create_tables(MODELS)
  return db