import pdfplumber


def get_book_chapter(chapter: int):
    with pdfplumber.open("static/books/master_margarita.pdf") as pdf:
        first_page = pdf.pages[chapter]
        return first_page.extract_text()
