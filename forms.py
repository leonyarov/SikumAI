# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    short_text = StringField('Short Text')
    msdn = StringField('MSDN')
    image = StringField('Image')
    file_name = StringField('File Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
