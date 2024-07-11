import pdfplumber
import os

def get_book_chapter(book_name, chapter: int):
    """
        Extracts text from a specific chapter of a book in PDF format.

        Parameters:
        book_name (str): The name of the book.
        chapter (int): The chapter number to extract.

        Returns:
        str: The text content of the specified chapter.
        """
    pdf_path = os.path.join("static", "books", f"{book_name}.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[chapter - 1]
        return first_page.extract_text()


def get_possible_chapter_list(book_name):
    pdf_path = os.path.join("static", "books", f"{book_name}.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        text = pdf.pages[0: 10]
        text = [page.extract_text() for page in text]
        return " ".join(text)
