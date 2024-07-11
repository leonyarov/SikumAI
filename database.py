from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

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

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    short_text = db.Column(db.String(500), nullable=True)
    msdn = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'pages': self.pages,
            'short_text': self.short_text,
            'msdn': self.msdn,
            'image': self.image
        }

    def __init__(self, author, title, pages, short_text=None, msdn=None, image="book.jpg"):
        self.author = author
        self.title = title
        self.pages = pages
        self.short_text = short_text
        self.msdn = msdn
        self.image = image


class PlotPoint(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = db.Column(db.String(36), db.ForeignKey('book.id'), nullable=False)
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

    def __init__(self, chapter_id, death_and_tragic_events=None, decisions=None, conflicts=None,
                 character_development=None, symbolism_and_imagery=None, foreshadowing=None, setting_description=None, chapter_summary=None, chapter_number=0, chapter_name=None):
        self.chapter_id = chapter_id
        self.death_and_tragic_events = death_and_tragic_events
        self.decisions = decisions
        self.conflicts = conflicts
        self.character_development = character_development
        self.symbolism_and_imagery = symbolism_and_imagery
        self.foreshadowing = foreshadowing
        self.setting_description = setting_description
        self.chapter_summary = chapter_summary
        self.chapter_number = chapter_number
        self.chapter_name = chapter_name


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
