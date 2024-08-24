import pdfplumber
import os

from functions.prompt_caching import get_chapter, save_chapter


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


def find_chapter(book_name, chapter_name, chapter_list: list):

    print("Searching for", chapter_name, "in", book_name, "with chapters", chapter_list)
    if get_chapter(book_name, chapter_name) is not None:
        return get_chapter(book_name, chapter_name).chapter_text
    temp_chapters = chapter_list.copy()
    pdf_path = os.path.join("static", "books", f"{book_name}.pdf")
    chapter_text = ""
    chapters = dict.fromkeys(chapter_list, 0)
    with (pdfplumber.open(pdf_path) as pdf):
        for i, page in enumerate(pdf.pages):
            temp_text = page.extract_text(y_tolerance=5).lower()
            if len(temp_chapters) == 0:
                break

            if i > 10 and len(chapter_list) - len(temp_chapters) > 2:
                temp_chapters = chapter_list.copy() # fake chapters

            for chapter in temp_chapters:
                if chapter.lower() in temp_text:
                    print(f"Found {chapter} at {i}")
                    chapters[chapter] = i
                    temp_chapters.pop(temp_chapters.index(chapter))
                    break
                if i == len(pdf.pages) - 1:
                    chapters[chapter] = -1
                    break
        for k, v in chapters.items():
            print(f"chapter {k} is at {v}")

        if chapters[chapter_name] == -1 or chapters[chapter_name] == 0:
            print("Chapter not found")
            return None  # chapter not found

        index = chapter_list.index(chapter_name)

        start = chapters[chapter_name]
        end = chapters[chapter_list[index + 1]]

        if index == len(chapter_list) - 1:
            end = len(pdf.pages) - 1
        elif end <= 0:
            end = index + 5
        print(f"Extracting {chapter_name} ({chapters[chapter_name]}) from {start} to {end}")
        for i in range(start, end + 1):
            page = pdf.pages[i].extract_text()
            chapter_text += page + " "
        save_chapter(book_name, chapter_text, chapter_name)
        return chapter_text
