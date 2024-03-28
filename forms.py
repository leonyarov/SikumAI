from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from database import Book


class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    short_text = StringField('Short Text')
    msdn = StringField('MSDN')
    submit = SubmitField('Submit')
