import os
import json
import requests
from dotenv import load_dotenv
import pdfplumber
from functions.book import get_book_chapter, get_possible_chapter_list
# Load environment variables from .env file
load_dotenv()




def build_prompt(book_name, chapter_name, page_number, page_content, next_page_content, previous_summaries):
    """
        Builds a prompt for generating a detailed summary of a book chapter.

        Parameters:
        book_name (str): The name of the book.
        chapter_name (str): The name of the chapter.
        page_number (int): The current page number.
        page_content (str): The content of the current page.
        next_page_content (str): The content of the next page.
        previous_summaries (list): A list of previous chapter summaries.

        Returns:
        str: The constructed prompt for the language model.
        """
    previous_summary_text = "\n\n".join(previous_summaries)
    prompt = (f"Summary of {book_name}, Chapter '{chapter_name}', Page {page_number}:\n\n{page_content}\n\n"
              f"Continued on next page:\n{next_page_content}\n\nPrevious summaries:\n{previous_summary_text}\n\n"
              "Please generate a detailed summary for this page, focusing on key plot points, "
              "character developments, and story-driven actions. Include any significant decisions made by characters, "
              "conflicts, emotional moments, and elements of foreshadowing or symbolism.")
    return prompt


def build_qa_prompt(book_name, chapter_name, detailed_summary):
    """
       Builds a prompt for generating educational questions and answers based on a chapter summary.

       Parameters:
       book_name (str): The name of the book.
       chapter_name (str): The name of the chapter.
       detailed_summary (str): The detailed summary of the chapter.

       Returns:
       str: The constructed prompt for the language model to generate Q&A.
       """
    prompt = (f"Based on the detailed summary of '{book_name}', Chapter '{chapter_name}', "
              "generate a set of educational questions and their corresponding answers. Focus on character motivations, "
              "plot implications, thematic elements, and any significant narrative techniques used in this chapter.\n\n"
              f"Detailed Summary:\n{detailed_summary}\n")
    return prompt


def build_chapter_list_prompt(book_name):
    """
        Builds a prompt for generating a list of possible chapters in a book.

        Parameters:
        book_name (str): The name of the book.

        Returns:
        str: The constructed prompt for the language model to generate a list of chapters.
        """
    chapter_list = get_possible_chapter_list(book_name)
    prompt = (f"Generate a list of possible chapters for the book '{book_name}'.\n"
              f"return a list of chapters in the format: 'Title 1,Title 2, ...'\n"
              f"Extracted text:\n{chapter_list}.\n"
              )

    return prompt


def generate_summary(prompt):
    """
        Generates a summary using the Google Language Model API.

        Parameters:
        prompt (str): The prompt to be sent to the API.

        Returns:
        str: The generated summary from the API.
        """
    google_api_key = os.getenv('GOOGLE_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    params = {"key": google_api_key}
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code == 200:
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        # save_prompt(prompt, summary)
        return summary
    else:
        err_msg = response.text
        # save_prompt(prompt, err_msg)
        return {"error": response.text}


def generate_chapter_summaries_and_qa(book_name, book_chapters, chapter_names):
    """
        Generates detailed summaries and educational Q&A for each chapter of a book.

        Parameters:
        book_name (str): The name of the book.
        book_chapters (list): A list of chapter numbers to process.
        chapter_names (list): A list of chapter names corresponding to the chapter numbers.

        Returns:
        tuple: Paths to the summary and Q&A output files.
        """
    chapter_summaries = []
    previous_summaries = []
    questions_and_answers = []

    for i, chapter_number in enumerate(book_chapters):
        chapter_content = get_book_chapter(book_name, chapter_number)
        next_chapter_content = get_book_chapter(book_name, book_chapters[i + 1]) if i < len(book_chapters) - 1 else ""
        detailed_summary_prompt = build_prompt(book_name, chapter_names[i], chapter_number, chapter_content,
                                               next_chapter_content, previous_summaries)
        detailed_summary = generate_summary(detailed_summary_prompt)
        chapter_summaries.append(detailed_summary)
        previous_summaries.append(detailed_summary)

        qa_prompt = build_qa_prompt(book_name, chapter_names[i], detailed_summary)
        qa_content = generate_summary(qa_prompt)
        questions_and_answers.append(qa_content)

    # Write summaries to the output file
    summary_file_name = f"{book_name}_summaries.txt"
    summary_file_path = os.path.join("chatbot", "output", summary_file_name)
    with open(summary_file_path, "w") as summary_file:
        for i, summary in enumerate(chapter_summaries):
            summary_file.write(f"Summary of Chapter {book_chapters[i]} - {chapter_names[i]}:\n{summary}\n\n")

    # Write Q&A to the output file
    qa_file_name = f"{book_name}_QA.txt"
    qa_file_path = os.path.join("chatbot", "output", qa_file_name)
    with open(qa_file_path, "w") as qa_file:
        for i, qa in enumerate(questions_and_answers):
            qa_file.write(f"Q&A for Chapter {book_chapters[i]} - {chapter_names[i]}:\n{qa}\n\n")

    return summary_file_path, qa_file_path


# Adjust the example usage accordingly
'''
book_name = "master_margarita"
book_chapters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
chapter_names = ["Never Talk to Strangers", "Pontius Pilate", "The Seventh Proof", "The Pursuit",
                 "The Affair at Griboyedov",
                 "Schizophrenia", "The Haunted Flat", "A Duel between Professor and Poet", "Koroviev's Tricks",
                 "News from Yalta"]
summary_file_path, qa_file_path = generate_chapter_summaries_and_qa(book_name, book_chapters, chapter_names)
print("Summaries saved to:", summary_file_path)
print("Q&A saved to:", qa_file_path)
'''