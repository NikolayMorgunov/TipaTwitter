from peewee import *

db = SqliteDatabase('users.db')


class User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db
