from news_db import *


def news_create_check(title):
    news_in_db = News.select().where(News.title == title)
    if news_in_db:
        return False
    return True
