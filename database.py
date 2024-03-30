from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
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

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

