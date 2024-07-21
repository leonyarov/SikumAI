import logging
import os
import re

import requests
from dotenv import load_dotenv

from Chatbot.prompt_generating import build_bagrut_answers_prompt, build_chapter_list_prompt, build_plot_points_prompt, \
    build_bagrut_questions_prompt
from database import BagrutQuestion, BagrutAnswer, PlotPoint, db
from functions.book import find_chapter
from functions.formatting import chapters_to_list
from functions.prompt_caching import get_prompt, save_prompt

# Load environment variables from ..env file
load_dotenv()


def get_chapter_list(book_name):
    prompt = build_chapter_list_prompt(book_name)
    result = execute_prompt(prompt)
    return chapters_to_list(result)


def execute_prompt(prompt):
    """
        Generates a summary using the Google Language Model API.

        Parameters:
        prompt (str): The prompt to be sent to the API.

        Returns:
        str: The generated summary from the API.
        """
    if get_prompt(prompt) is not None:
        return get_prompt(prompt).response
    google_api_key = os.getenv('GOOGLE_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    params = {"key": google_api_key}
    tries, max_tries = 0, 3
    response = requests.post(url, headers=headers, params=params, json=payload)
    while tries < max_tries:
        print(f"({tries+1}) Executing prompt {prompt[:40]}...")
        try:
            if response.status_code == 200:
                summary = response.json()['candidates'][0]['content']['parts'][0]['text']
                save_prompt(prompt, summary)
                logging.debug(f"API Response:{summary}")
                return summary
            else:
                response = requests.post(url, headers=headers, params=params, json=payload)
                tries += 1
                continue
        except:
            err_msg = response.text
            logging.error(f"API Response:{err_msg}")
            print(response.json())
    return "Could not get answer from API, try again later"


def generate_plot_points(book_name, chapter_name, chapter_list):
    """
    Generates plot points for a book chapter and saves them to the database.

    Parameters:
    book_id (str): The ID of the book.
    chapter_name (str): The name of the chapter.
    chapter_number (int): The number of the chapter.
    page_content (str): The content of the current page.

    Returns:
    str: A success message or error.
    """
    page_content = find_chapter(book_name, chapter_name, chapter_list)

    plot_points_prompt = build_plot_points_prompt(book_name, chapter_name, page_content)
    plot_points_response = execute_prompt(plot_points_prompt)

    if "error" in plot_points_response:
        return plot_points_response["error"]

    print(plot_points_response)

    # Assuming the plot_points_response is a structured text or JSON that we can parse
    plot_points_data = parse_plot_points_response(plot_points_response)

    plot_point = PlotPoint(
        book_id=book_name,
        chapter_name=chapter_name,
        death_and_tragic_events=plot_points_data.get('death_and_tragic_events'),
        decisions=plot_points_data.get('decisions'),
        conflicts=plot_points_data.get('conflicts'),
        character_development=plot_points_data.get('character_development'),
        symbolism_and_imagery=plot_points_data.get('symbolism_and_imagery'),
        foreshadowing=plot_points_data.get('foreshadowing'),
        setting_description=plot_points_data.get('setting_description'),
        chapter_summary=plot_points_data.get('chapter_summary')
    )
    print("Plot points generated and saved successfully.")
    return plot_point, plot_points_data


def parse_plot_points_response(response):
    """
    Parses the response from the API into structured plot points data.

    Parameters:
    response (str): The response from the API.

    Returns:
    dict: Parsed plot points data.
    """
    import re

    logging.debug(f"Raw API Response: {response}")

    # Initialize the dictionary with empty strings
    plot_points_data = {
        'death_and_tragic_events': '',
        'decisions': '',
        'conflicts': '',
        'character_development': '',
        'symbolism_and_imagery': '',
        'foreshadowing': '',
        'setting_description': '',
        'chapter_summary': ''
    }

    # Use regex to find sections and their content
    sections = re.split(r'\*\*\d+\.\s([A-Za-z\s]+)\*\*', response)

    section_names = {
        "Death and Tragic Events": 'death_and_tragic_events',
        "Decisions": 'decisions',
        "Conflicts": 'conflicts',
        "Character Development": 'character_development',
        "Symbolism and Imagery": 'symbolism_and_imagery',
        "Foreshadowing": 'foreshadowing',
        "Setting Description": 'setting_description',
        "Chapter Summary": 'chapter_summary'
    }

    current_section = None
    for i, section in enumerate(sections):
        section = section.strip()
        if section in section_names:
            current_section = section_names[section]
        elif current_section:
            plot_points_data[current_section] += section

    logging.debug(f"Parsed Plot Points Data: {plot_points_data}")
    return plot_points_data
    # ToDo - Save to DataBase


def generate_bagrut_qa(book_name, chapter_name, plot_points_data):
    questions_and_answers = []

    # Generate Bagrut-level questions
    bagrut_questions_prompt = build_bagrut_questions_prompt(book_name, chapter_name, plot_points_data)
    bagrut_questions_response = execute_prompt(bagrut_questions_prompt)
    bagrut_questions = re.split(r'\n+', bagrut_questions_response)

    for question in bagrut_questions:
        if question.strip():
            bagrut_question = BagrutQuestion(book_id=book_name, chapter_name=chapter_name, question=question)
            db.session.add(bagrut_question)
            db.session.commit()

            # Generate Bagrut answers
            bagrut_answers_prompt = build_bagrut_answers_prompt(book_name, chapter_name, plot_points_data, question)
            bagrut_answers_response = execute_prompt(bagrut_answers_prompt)
            bagrut_answer = BagrutAnswer(question_id=bagrut_question.id, answer=bagrut_answers_response)
            db.session.add(bagrut_answer)
            db.session.commit()

            questions_and_answers.append({
                "question": question,
                "answer": bagrut_answers_response
            })

    return questions_and_answers


def generate_chapter_summaries_and_qa(book_name, chapter):
    """
    Generates summaries, Plot Points & Bagrut Style Questions and Answers questions

    Parameters:
    book_name (str): The name of the book.
    chapter (tuple): A tuple containing chapter number and chapter title.

    Returns:
    dict: A dictionary containing chapter summaries, questions and answers, and Bagrut questions and answers.
    """
    pass
