import os.path

from flask import Flask, request, url_for, redirect, get_flashed_messages, session, jsonify, flash
from flask import render_template
from flask_cors import CORS, cross_origin

from chatbot.chatbot import generate_plot_points, get_chapter_list, generate_chapter_bagrutQnA
from chatbot.responses.lesson_plan import lesson_plan_prompt
from database import db, Book, PlotPoint, LessonPlan
from forms import BookForm
from functions.book import *
import json

app = Flask(__name__, static_url_path="/static")
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = 'SECRET!'

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
    if not session.get('prompt'):
        session['prompt'] = None

    return render_template('main/index.html', book_form=book_form, library_images=library_images, books=books)


@app.route('/books')
@cross_origin()
def books():
    b = Book.query.all()
    # print(b)
    # return b
    return jsonify(b)


@cross_origin()
@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    gen_type = data['type']
    pages = data['pages']
    file = ""
    if gen_type == "qa":
        file = "chatbot/output/master_margarita_QA.txt"
    elif gen_type == "cs":
        file = "chatbot/output/master_margarita_summaries.txt"
    elif gen_type == "lp":
        file = "chatbot/output/master_margarita_summaries.txt"

    with open(file, "r", encoding='utf-8') as f:
        text = f.read()

    return jsonify(text)


@cross_origin()
@app.route('/get_page', methods=['POST'])
def change_chapter():
    data = request.get_json()
    page = data['page']
    book_id = data['book']
    book = Book.query.filter_by(id=book_id).first()
    chapters = get_chapter_list(book.file_name)

    if page >= len(chapters):
        return jsonify("End of book")

    chapter = find_chapter(book_name=book.file_name, chapter_name=chapters[page], chapter_list=chapters)
    return jsonify(chapter)


@app.route('/add_book', methods=['POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            author=form.author.data,
            title=form.title.data,
            pages=form.pages.data,
            short_text=form.short_text.data,
            msdn=form.msdn.data,
            image=form.image.data,
            file_name=form.file_name.data  # Ensure this line is present
        )
        try:
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully", 'success')
        except Exception as e:
            flash("Book not uploaded", 'danger')
            db.session.rollback()
    else:
        flash("Book unvalidated", 'danger')

    return redirect("/")


@app.route('/set_book', methods=['POST'])
def set_book():
    book_id = request.form['book']
    book = Book.query.filter_by(id=book_id).first()
    session['book'] = book.to_dict()
    return redirect("/")


@app.route('/upload_book', methods=['POST'])
def upload_book():
    if 'book' not in request.files or 'cover' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    book = request.files['book']
    cover = request.files['cover']

    cover_folder = os.path.join(app.root_path, 'static')
    book_folder = os.path.join(app.root_path, 'static', 'books')

    cover_path = os.path.join(cover_folder, cover.filename)
    book_path = os.path.join(book_folder, book.filename)

    book.save(book_path)
    cover.save(cover_path)

    try:
        new_book = Book(
            author=request.form['author'],
            title=request.form['title'],
            pages=100,
            short_text=request.form['short_text'],
            msdn=request.form['msdn'],
            image=cover.filename,
            file_name=os.path.splitext(book.filename)[0]
        )
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify("ok")


@cross_origin
@app.route('/generate_summary', methods=['POST'])
def plot_points():
    data = request.get_json()
    book_id = data['book_id']
    chapter_name = data['chapter_name']

    book = Book.query.filter_by(id=book_id).first()

    result = generate_plot_points(book.file_name, chapter_name)

    return jsonify({'result': result[0]})


@cross_origin
@app.route('/generate_questions', methods=['POST'])
def questions():
    data = request.get_json()
    book_id = data['book_id']
    chapter_name = data['chapter_name']

    book = Book.query.filter_by(id=book_id).first()

    result = generate_chapter_bagrutQnA(book.file_name, chapter_name)

    return jsonify({'result': result})


@cross_origin
@app.route("/get_chapters", methods=['POST'])
def get_chapters():
    data = request.get_json()
    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()
    try:
        chapters = get_chapter_list(book_name=book.file_name)
        return jsonify(chapters)
    except:
        return jsonify([])


@cross_origin
@app.route('/translate', methods=['POST'])
def translate():
    from translate import Translator

    data = request.get_json()
    # print(data)
    text = data['text']
    translator = Translator(to_lang='he')
    to_send = dict()
    for k, v in text.items():
        if len(v) >= 499:
            bins = [v[i:i + 499] for i in range(0, len(v), 499)]
            t = "".join([translator.translate(b) for b in bins])
            to_send[k] = t
            continue
        to_send[k] = translator.translate(v)


    return jsonify({'result': to_send})

@cross_origin
@app.route('/generate_lesson_plan', methods=['POST'])
def generate_lesson_plan():
    data = request.get_json()

    book_id = data['book_id']
    chapter_name = data['chapter_name']

    book = Book.query.filter_by(id=book_id).first()
    result = lesson_plan_prompt(book_name=book.file_name, chapter=chapter_name)
    if result is None:
        result = "Error generating lesson plan"

    return jsonify({'result': result})


@cross_origin
@app.route('/list_books', methods=['GET'])
def list_books():
    books = Book.query.all()
    books_list = [{"id": book.id, "title": book.title} for book in books]
    return jsonify(books_list)


@cross_origin
@app.route('/get_book', methods=['POST'])
def get_book_file():
    data = request.get_json()
    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()
    return jsonify(book.file_name + '.pdf')


@cross_origin
@app.route('/history', methods=['POST'])
def history():
    data = request.get_json()
    book_id = data['book_id']
    content = data['content']

    book = Book.query.filter_by(id=book_id).first().file_name
    if content == 'cs':
        result = PlotPoint.query.filter_by(book_name=book).all()
        return jsonify(result)
    elif content == 'lp':
        result = LessonPlan.query.filter_by(book_name=book).all()
        return jsonify(result)
    else:
        return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)
