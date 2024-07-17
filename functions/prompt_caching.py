from sqlalchemy.orm import sessionmaker

from database import Prompt, db, BookChapter
from sqlalchemy import create_engine


def save_prompt(prompt, result):
    p = Prompt(prompt=prompt, response=result)
    try:
        db.session.add(p)
        db.session.commit()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(p)
        session.commit()


def save(obj, overwrite=False):
    try:
        db.session.add(obj)
        db.session.commit()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(obj)
        session.commit()


def get_prompt(prompt):
    try:
        p = Prompt.query.filter_by(prompt=prompt).first()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        p = session.query(Prompt).filter_by(prompt=prompt).first()
    return p


def save_chapter(book_name, chapter_text, chapter_title):
    p = BookChapter(book_name=book_name, chapter_text=chapter_text, chapter_title=chapter_title)
    try:
        db.session.add(p)
        db.session.commit()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(p)
        session.commit()


def get_chapter(book_name, chapter_title):
    try:
        p = BookChapter.query.filter_by(book_name=book_name, chapter_title=chapter_title).first()
    except:
        engine = create_engine('sqlite:///instance/database.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        p = session.query(BookChapter).filter_by(book_name=book_name, chapter_title=chapter_title).first()
    return p
