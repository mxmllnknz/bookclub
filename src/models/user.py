from peewee import DateTimeField, TextField, Model
from typing import Tuple
import datetime

class User(Model):
    created_at = DateTimeField(null=False, default=datetime.datetime.now())
    updated_at = DateTimeField(null=False, default=datetime.datetime.now())
    deleted_at = DateTimeField(null=True)
    name = TextField(null=False, unique=True)
    formatted_name = TextField(null=False, unique=True)
        
def createOrGetUser(name: str) -> Tuple[User, bool]:
    return User.get_or_create(
        name = name, 
        defaults={'formatted_name': str(name).split('#')[0]})