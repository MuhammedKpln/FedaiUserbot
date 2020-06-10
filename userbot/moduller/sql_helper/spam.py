from typing import Union

try:
    from userbot.moduller.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import Query


class Spams(BASE):
    __tablename__ = "spams"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    spam_name: str = Column(String, nullable=False)
    spam: str = Column(Text, nullable=False)

    def __init__(self, spam_name: str, spam: str = ''):
        self.spam_name = spam_name
        self.spam = spam


Spams.__table__.create(checkfirst=True)


def get_spam(spam_name: str) -> Union[bool, str]:
    try:
        spam = SESSION.query(Spams).filter_by(spam_name=spam_name).first()

        if not spam:
            return False

        return spam.spam

    finally:
        SESSION.close()


def get_spams() -> Query:
    try:
        return SESSION.query(Spams).all()
    finally:
        SESSION.close()


def add_spam(spam_name: str, spam: str) -> bool:
    try:
        if get_spam(spam_name):
            return False

        new_spam = Spams(spam_name, spam)
        SESSION.add(new_spam)
        SESSION.commit()

        return True

    except Exception as e:
        print(e)
        return False


def remove_spam(spam_name: str) -> bool:
    check_for_spam = get_spam(spam_name)

    if check_for_spam:
        SESSION.query(Spams).filter_by(spam_name=spam_name).delete()
        SESSION.commit()
        return True

    return False
