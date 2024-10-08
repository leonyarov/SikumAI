import uuid
from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class Book(db.Model):
    id: str
    author: str
    title: str
    pages: int
    short_text: str
    msdn: str
    image: str
    file_name: str

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    short_text = db.Column(db.String(500), nullable=True)
    msdn = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(100), nullable=True)
    file_name = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'pages': self.pages,
            'short_text': self.short_text,
            'msdn': self.msdn,
            'image': self.image,
            'file_name': self.file_name
        }

    def __init__(self, author, title, pages, short_text=None, msdn=None, image="book.jpg",
                 file_name=None):
        self.author = author
        self.title = title
        self.pages = pages
        self.short_text = short_text
        self.msdn = msdn
        self.image = image
        self.file_name = file_name


@dataclass
class PlotPoint(db.Model):
    id: str
    book_name: str
    chapter_name: str
    chapter_number: int
    death_and_tragic_events: str
    decisions: str
    conflicts: str
    character_development: str
    symbolism_and_imagery: str
    foreshadowing: str
    setting_description: str
    chapter_summary: str

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_name = db.Column(db.String(100), nullable=False)
    chapter_name = db.Column(db.String(100), nullable=True)
    chapter_number = db.Column(db.Integer, default=0)
    death_and_tragic_events = db.Column(db.Text, nullable=True)
    decisions = db.Column(db.Text, nullable=True)
    conflicts = db.Column(db.Text, nullable=True)
    character_development = db.Column(db.Text, nullable=True)
    symbolism_and_imagery = db.Column(db.Text, nullable=True)
    foreshadowing = db.Column(db.Text, nullable=True)
    setting_description = db.Column(db.Text, nullable=True)
    chapter_summary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"PlotPoint('{self.id}', chapter {self.chapter_number}: '{self.chapter_name}')"

    def __init__(self, book_name, chapter_name=None, chapter_number=0,
                 death_and_tragic_events=None, decisions=None, conflicts=None,
                 character_development=None, symbolism_and_imagery=None,
                 foreshadowing=None, setting_description=None, chapter_summary=None):
        self.book_name = book_name
        self.chapter_name = chapter_name
        self.chapter_number = chapter_number
        self.death_and_tragic_events = death_and_tragic_events
        self.decisions = decisions
        self.conflicts = conflicts
        self.character_development = character_development
        self.symbolism_and_imagery = symbolism_and_imagery
        self.foreshadowing = foreshadowing
        self.setting_description = setting_description
        self.chapter_summary = chapter_summary



class Question(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = db.Column(db.String(36), db.ForeignKey('book.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Question('{self.id}', '{self.question}')"

    def __init__(self, book_id, question, answer):
        self.book_id = book_id
        self.question = question
        self.answer = answer


class Prompt(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Prompt('{self.id}', '{self.prompt}')"

    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response


class BookChapter(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_name = db.Column(db.String(100), nullable=False)
    chapter_title = db.Column(db.String(100), nullable=False)
    chapter_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BookChapter('{self.id}', '{self.chapter_title}')"

    def __init__(self, book_name, chapter_title, chapter_text):
        self.book_name = book_name
        self.chapter_title = chapter_title
        self.chapter_text = chapter_text


@dataclass
class LessonPlan(db.Model):
    id: str
    book_name: str
    reading: str
    discussion: str
    bagrut: str
    writing: str

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_name = db.Column(db.String(100), nullable=False)
    reading = db.Column(db.Text, nullable=False)
    discussion = db.Column(db.Text, nullable=False)
    bagrut = db.Column(db.Text, nullable=False)
    writing = db.Column(db.Text, nullable=False)

    def __init__(self, book_name, reading, discussion, bagrut, writing):
        self.book_name = book_name
        self.reading = reading
        self.discussion = discussion
        self.bagrut = bagrut
        self.writing = writing

    def __repr__(self):
        return f"LessonPlan('{self.id}', '{self.book_name}')"


class BagrutAnswer(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = db.Column(db.String(36), db.ForeignKey('bagrut_question.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BagrutAnswer('{self.id}', '{self.answer}')"

    def __init__(self, question_id, answer):
        self.question_id = question_id
        self.answer = answer


class BagrutQuestion(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = db.Column(db.String(36), db.ForeignKey('book.id'), nullable=False)
    chapter_name = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BagrutQuestion('{self.id}', '{self.chapter_name}', '{self.question}')"

    def __init__(self, book_id, chapter_name, question):
        self.book_id = book_id
        self.chapter_name = chapter_name
        self.question = question
