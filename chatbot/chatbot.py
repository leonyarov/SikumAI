import logging
import os
import re

import requests
from dotenv import load_dotenv

from chatbot.prompt_generating import build_bagrut_answers_prompt, build_chapter_list_prompt, build_plot_points_prompt, \
    build_bagrut_questions_prompt
from database import PlotPoint, BagrutQuestion, BagrutAnswer
from functions.book import find_chapter
from functions.formatting import chapters_to_list
from functions.prompt_caching import get_prompt, save_prompt, save

# Load environment variables from ..env file
load_dotenv()


def get_chapter_list(book_name):
    prompt = build_chapter_list_prompt(book_name)
    result = execute_prompt(prompt)
    return chapters_to_list(result)


def execute_prompt(prompt, override: bool = False):
    """
        Generates a summary using the Google Language Model API.

        Parameters:
        prompt (str): The prompt to be sent to the API.

        Returns:
        str: The generated summary from the API.
        """
    if get_prompt(prompt) is not None and not override:
        return get_prompt(prompt).response
    google_api_key = os.getenv('GOOGLE_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    params = {"key": google_api_key}
    tries, max_tries = 0, 3
    response = requests.post(url, headers=headers, params=params, json=payload)
    while tries < max_tries:
        print(f"({tries + 1}) Executing prompt {prompt[:40]}...")
        try:
            if response.status_code == 200:
                summary = response.json()['candidates'][0]['content']['parts'][0]['text']
                print("Raw API Response:", summary)
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


def generate_plot_points(book_name, chapter_name):
    chapter_list = get_chapter_list(book_name)
    page_content = find_chapter(book_name, chapter_name, chapter_list)

    plot_points_prompt = build_plot_points_prompt(book_name, chapter_name, page_content)
    plot_points_response = execute_prompt(plot_points_prompt, override=True)

    if "Error" in plot_points_response:
        return None, {"error": plot_points_response}

    plot_points_data = parse_plot_points_response(plot_points_response)

    # Assuming chapter_number can be derived from chapter_name or needs to be passed as an argument
    chapter_number = chapter_list.index(chapter_name) + 1 if chapter_name in chapter_list else 0

    plot_point = PlotPoint(
        book_name=book_name,
        chapter_name=chapter_name,
        chapter_number=chapter_number,
        death_and_tragic_events=plot_points_data.get('death_and_tragic_events'),
        decisions=plot_points_data.get('decisions'),
        conflicts=plot_points_data.get('conflicts'),
        character_development=plot_points_data.get('character_development'),
        symbolism_and_imagery=plot_points_data.get('symbolism_and_imagery'),
        foreshadowing=plot_points_data.get('foreshadowing'),
        setting_description=plot_points_data.get('setting_description'),
        chapter_summary=plot_points_data.get('chapter_summary')
    )

    print("PlotPoint Instance:", plot_point)
    print("Plot points generated and saved successfully.")
    save(plot_point)
    return plot_point, plot_points_data


def parse_plot_points_response(response):
    import re

    logging.debug(f"Raw API Response: {response}")

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

    # Pattern to match section headers
    pattern = re.compile(r'\*\*([A-Za-z\s]+):\*\*')

    # Find all section headers and their start positions
    matches = list(pattern.finditer(response))
    sections = {match.group(1): match.start() for match in matches}

    logging.debug(f"Sections identified: {sections}")

    # Extract content for each section
    for i, section in enumerate(sections):
        start_pos = sections[section]
        end_pos = sections[list(sections.keys())[i + 1]] if i + 1 < len(sections) else len(response)
        content = response[start_pos:end_pos]
        section_key = section.strip().lower().replace(' ', '_')

        if section_key in plot_points_data:
            plot_points_data[section_key] = content.split('**')[-1].strip()
            logging.debug(f"Content for {section_key}: {plot_points_data[section_key]}")

    for key in plot_points_data:
        plot_points_data[key] = plot_points_data[key].strip()

    logging.debug(f"Parsed Plot Points Data: {plot_points_data}")
    return plot_points_data


def generate_bagrut_qa(book_name, chapter_name, plot_points_data):
    # Generate Bagrut-level questions
    questions_and_answers = []
    bagrut_examples = [
        {
            "question": "Choose a short story you studied that centers on the human need for understanding, warmth, love, or comfort. What need is expressed in the story you chose, and how does it affect the behavior of a central character in the story? Explain and illustrate your answer.",
            "type": "open-ended"
        },
        {
            "question": "Explain and illustrate one way in which this human need is expressed in the story.",
            "type": "open-ended"
        },
        {
            "question": "Choose a pivotal event that changes the course of a central character's life in a short story you studied, describe how the character copes with this event, and explain why you think it is pivotal in their life.",
            "type": "open-ended"
        },
        {
            "question": "Explain and illustrate one way in which the character's coping with the event is expressed in the story.",
            "type": "open-ended"
        },
        {
            "question": "Describe the physical journey of the protagonist in the story, and explain what mental journey they undergo as a result of their physical journey.",
            "type": "open-ended"
        },
        {
            "question": "Choose a character from the reading book you studied that evoked empathy in you and a character that evoked rejection. Describe each of these characters and explain what about them evoked these feelings in you.",
            "type": "open-ended"
        },
        {
            "question": "What insights about human nature and/or society arise from the reading book you studied? Explain your answer and base it on the relationships between the characters and the ending of the reading book.",
            "type": "open-ended"
        }
    ]
    bagrut_questions_prompt = build_bagrut_questions_prompt(book_name, chapter_name, plot_points_data, bagrut_examples)

    bagrut_questions_response = execute_prompt(bagrut_questions_prompt)
    bagrut_questions = re.split(r'\n+', bagrut_questions_response)

    for question in bagrut_questions:
        if question.strip():
            bagrut_question = BagrutQuestion(book_id=book_name, chapter_name=chapter_name, question=question)
            # ToDo -  save(bagrut_question)
            # Generate Bagrut answers
            bagrut_answers_prompt = build_bagrut_answers_prompt(book_name, chapter_name, plot_points_data, question)
            bagrut_answers_response = execute_prompt(bagrut_answers_prompt)
            bagrut_answer = BagrutAnswer(question_id=bagrut_question.id, answer=bagrut_answers_response)
            # ToDo -  save(bagrut_answer)
            questions_and_answers.append({
                "question": question,
                "answer": bagrut_answers_response
            })

    return questions_and_answers


def generate_chapter_bagrutQnA(book_name, chapter):
    """
    Generates summaries, Plot Points & Bagrut Style Questions and Answers questions

    Parameters:
    book_name (str): The name of the book.
    chapter (tuple): A tuple containing chapter number and chapter title.

    Returns:
    dict: A dictionary containing chapter summaries, plot points, questions and answers, and Bagrut questions and answers.
    """

    # Generate plot points
    plot_point, plot_points_data = generate_plot_points(book_name, chapter)

    if plot_point is None:
        return plot_points_data  # Return the error message

    # Generate Bagrut-style questions and answers using plot points
    questions_and_answers = generate_bagrut_qa(book_name, chapter, plot_points_data)

    return questions_and_answers
