from peewee import *

db = SqliteDatabase('news.db')


class News(Model):
    username = CharField()
    title = CharField()
    text = CharField()

    class Meta:
        database = db
