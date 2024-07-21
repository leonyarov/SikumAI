from flask import Flask, request, url_for, redirect, get_flashed_messages, session, jsonify, flash
from flask import render_template
from flask_cors import CORS, cross_origin

from chatbot.chatbot import generate_plot_points, get_chapter_list, generate_chapter_summaries_and_qa
from chatbot.responses.lesson_plan import lesson_plan_prompt
from chatbot.chatbot import generate_plot_points, get_chapter_list, generate_chapter_summaries_plotPoints_bagrutQnA
from chatbot.responses.lesson_plan import lesson_plan_prompt
from database import db, Book
from forms import BookForm
from functions.book import *

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


@app.route('/prompt', methods=['POST'])
@cross_origin()
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

    # text = text.replace('\r', '')
    # text = text.replace('\n\n\n', '\n')
    # text = text.replace('\n\n', '\n')
    return jsonify(text)


@app.route('/get_page', methods=['POST'])
@cross_origin()
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


@cross_origin
@app.route('/generate_summary', methods=['POST'])
def plot_points():
    data = request.get_json()
    book_id = data['book_id']
    chapter_name = data['chapter_name']

    book = Book.query.filter_by(id=book_id).first()

    result = generate_plot_points(book.file_name, chapter_name)

    return jsonify({'result': result})


@cross_origin
@app.route("/get_chapters", methods=['POST'])
def get_chapters():
    data = request.get_json()
    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()
    chapters = get_chapter_list(book_name=book.file_name)
    return jsonify(chapters)


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


import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/generate_bagrut_qa', methods=['POST'])
@cross_origin()
def generate_bagrut_qa():
    try:
        data = request.get_json()
        book_id = data['book_id']
        book_chapters = data['chapters']
        chapter_names = data['chapter_names']

        # Debug logging
        logging.debug(f"Received data: {data}")

        # Fetch book details
        book = Book.query.filter_by(id=book_id).first()

        # Check if book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        summary_file_path, qa_file_path, bagrut_qa_file_path = generate_chapter_summaries_plotPoints_bagrutQnA(
            book_name=book.file_name,
            book_chapters=book_chapters,
        )

        return jsonify({
            'summary_file_path': summary_file_path,
            'qa_file_path': qa_file_path,
            'bagrut_qa_file_path': bagrut_qa_file_path
        })
    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/list_books', methods=['GET'])
@cross_origin()
def list_books():
    books = Book.query.all()
    books_list = [{"id": book.id, "title": book.title} for book in books]
    return jsonify(books_list)


if __name__ == '__main__':
    app.run(debug=True)
