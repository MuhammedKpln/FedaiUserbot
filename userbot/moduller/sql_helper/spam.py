try:
    from userbot.moduller.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, UnicodeText, Numeric, String, Integer, Text


class Spams(BASE):
    __tablename__ = "spams"
    id = Column(Integer , primary_key=True)
    spamName = Column(String, nullable=False)
    spam = Column(Text)

    def __init__(self, chat_id, spamName, spam):
        self.spamName = spamName
        self.spam = spam

    def __eq__(self, other):
        return bool(
            isinstance(other, Spams) and self.chat_id == other.chat_id
            and self.spamName == other.spamName)


Spams.__table__.create(checkfirst=True)


def get_spam(spamName, keyword):
    try:
        return SESSION.query(Spams).get(spamName)
    finally:
        SESSION.close()


def get_spams(chat_id):
    try:
        return SESSION.query(Spams).all()
    finally:
        SESSION.close()


def add_spam(spamName, spam):
    to_check = get_spam(spamName)
    print('tocheck', to_check)
    if not to_check:
        adder = Spams(spamName, spam)
        SESSION.add(adder)
        SESSION.commit()
        return True

    return False


def remove_spam(spamName):
    to_check = get_spam(spamName)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Spams).get(spamName)
        SESSION.delete(rem)
        SESSION.commit()
        return True
