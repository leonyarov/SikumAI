from flask import Flask, flash, request, url_for, redirect, get_flashed_messages, session, jsonify
from flask import render_template
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from forms import BookForm
from database import db, Book
from functions.book import *
app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'SECRET!'
csrf = CSRFProtect(app)

google_api_key = "AIzaSyD9iKE1Jnsx41e7yc_eDyfX4zB0zy9ZNXA"


@app.route('/', methods=['GET'])
def main_page():  # put application's code here
    get_flashed_messages()
    library_images = url_for('static', filename='book.jpg')
    books = Book.query.all()
    book_form = BookForm()
    if not session.get('book'):
        session['book'] = None
    if not session.get('chapter'):
        session['chapter'] = None
    if not session.get('page'):
        session['page'] = 0

    return render_template('main/index.html', book_form=book_form, library_images=library_images, books=books)


@app.route('/prompt', methods=['POST'])
def prompt():
    flash("You have been prompted", 'info')
    return redirect('/')


@app.route('/change_chapter', methods=['POST'])
@csrf.exempt
def change_chapter():
    chapter_num = request.form.get('page', "1")

    if chapter_num == "next":
        session['page'] = int(session['page']) + 1
    elif chapter_num == "prev":
        session['page'] = min(int(session['page']) - 1, 0)
    else:
        session['page'] = int(chapter_num)

    session['chapter'] = get_book_chapter(session['page'])

    print("Page selected: ", session['page'])

    return redirect('/')


@app.route('/set_book', methods=['POST'])
@csrf.exempt
def set_book():
    book_id = request.form['book']
    book = Book.query.filter_by(id=book_id).first()
    session['book'] = book.to_dict()
    return redirect("/")


@app.route('/add_book', methods=['POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Create a new book
        new_book = Book(
            author=form.author.data,
            title=form.title.data,
            pages=form.pages.data,
            short_text=form.short_text.data,
            msdn=form.msdn.data,
            image=form.image.data
        )
        try:
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            flash("book not uploaded", 'danger')
            db.session.rollback()
            db.session.flush()
            flash("book in db", "danger")
    else:
        flash("book unvalidated", 'danger')
        # Add and commit the new book to the database
        # Redirect to the list of books
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
