import logging
import os

import requests
from dotenv import load_dotenv

from chatbot.prompt_generating import build_chapter_list_prompt, build_plot_points_prompt
from database import PlotPoint
from functions.book import find_chapter
from functions.formatting import chapters_to_list
from functions.prompt_caching import get_prompt, save_prompt, save

# Load environment variables from ..env file
load_dotenv()
bagrut_qa_list = []  # Global list to store the generated Q&A
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
    cached_response = get_prompt(prompt)
    if cached_response is not None and not override:
        return cached_response.response

    google_api_key = os.getenv('GOOGLE_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    params = {"key": google_api_key}
    tries, max_tries = 0, 3

    while tries < max_tries:
        print(f"Executing prompt {prompt[:40]}...")
        try:
            response = requests.post(url, headers=headers, params=params, json=payload)
            if response.status_code == 200:
                summary = response.json()['candidates'][0]['content']['parts'][0]['text']
                print("Raw API Response:\n\n", summary)
                save_prompt(prompt, summary)
                logging.debug(f"API Response:{summary}")
                return summary
            else:
                logging.warning(f"Unexpected status code {response.status_code}: {response.text}")
                tries += 1
        except Exception as e:
            logging.error(f"API Request failed with error: {e}")
            tries += 1

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

    # print("PlotPoint Instance:", plot_point)
    # print("Plot points generated and saved successfully.\n\n")
    save(plot_point)
    return plot_point, plot_points_data


def parse_plot_points_response(response):
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

    pattern = re.compile(r'\*\*([A-Za-z\s]+):\*\*')
    matches = list(pattern.finditer(response))
    sections = {match.group(1).strip().lower().replace(' ', '_'): match.start() for match in matches}

    logging.debug(f"Sections identified: {sections}")

    for i, section in enumerate(sections):
        start_pos = sections[section]
        end_pos = sections[list(sections.keys())[i + 1]] if i + 1 < len(sections) else len(response)
        content = response[start_pos:end_pos].split('**')[-1].strip()
        plot_points_data[section] = content

    for key in plot_points_data:
        plot_points_data[key] = plot_points_data[key].strip()

    logging.debug(f"Parsed Plot Points Data: {plot_points_data}")
    return plot_points_data


import re


def parse_questions_and_answers(response_text):
    """
    Parses the AI's response to extract questions and answers separately.
    The questions are identified by the bullet point (*) and are followed by their respective answers.
    """
    questions_and_answers = []

    # Refine the regex to match both questions and answers more accurately
    pattern = re.compile(r'\*\s*(.+?)\*\*(.*?)\n', re.DOTALL)
    matches = pattern.findall(response_text)

    # Iterate through the matches and organize them into Q&A pairs
    for match in matches:
        question = match[0].strip()
        answer = match[1].strip()

        if question and answer:
            questions_and_answers.append({
                "question": question,
                "answer": answer
            })

    return questions_and_answers


def format_bagrut_output(questions_and_answers):
    """
    Formats the Bagrut Q&A output into a more readable format for front-end, ensuring each question is followed by its respective answer.
    """
    formatted_output = []

    # Loop through each QA pair and format it properly
    for idx, qa_pair in enumerate(questions_and_answers, 1):
        question = qa_pair.get('question', '').strip()
        answer = qa_pair.get('answer', '').strip()

        # Ensure both question and answer exist before formatting
        if question and answer:
            formatted_output.append(f"Q{idx}: {question}")
            formatted_output.append(f"A{idx}: {answer}\n")

    # Join all parts into a single string for easier front-end rendering
    return "\n".join(formatted_output)


def generate_bagrut_qa(book_name, chapter_name, plot_points_data):
    # Loop through each question and generate Q&A one by one
    for example in bagrut_examples:
        question_text = example['question']
        generate_single_bagrut_qa(book_name, chapter_name, question_text)

    # After generating all Q&A pairs, format them for display
    return display_all_bagrut_qa()


def display_all_bagrut_qa():
    """
    Displays all saved Bagrut-style questions and answers.
    """
    global bagrut_qa_list
    formatted_output = []

    for idx, qa_pair in enumerate(bagrut_qa_list, 1):
        question = qa_pair['question'].strip()
        answer = qa_pair['answer'].strip()

        formatted_output.append(f"Q{idx}: {question}")
        formatted_output.append(f"A{idx}: {answer}\n")

    # Return all Q&A in a readable format
    return "\n".join(formatted_output)


# Generate and format the final output
def generate_chapter_bagrutQnA(book_name, chapter):
    """
    Generates summaries, Plot Points & Bagrut Style Questions and Answers.
    """
    # Generate plot points
    plot_point, plot_points_data = generate_plot_points(book_name, chapter)

    if plot_point is None:
        return f"Error generating plot points for {chapter}: {plot_points_data.get('error', 'Unknown error')}"

    # Generate Bagrut-style questions and answers using plot points
    final_output = generate_bagrut_qa(book_name, chapter, plot_points_data)

    return final_output


def generate_single_bagrut_qa(book_name, chapter_name, question):
    """
    Generates a single Bagrut-style question and its answer based on plot points.
    """
    try:
        # Generate the question prompt
        bagrut_question_prompt = f"Generate a question for the following: {question}"
        bagrut_question_response = execute_prompt(bagrut_question_prompt)

        # Generate the answer prompt
        bagrut_answer_prompt = f"Generate an answer for the following question: {bagrut_question_response}"
        bagrut_answer_response = execute_prompt(bagrut_answer_prompt)

        # Save the result in memory
        save_bagrut_qa(bagrut_question_response, bagrut_answer_response)

        return {
            "question": bagrut_question_response,
            "answer": bagrut_answer_response
        }
    except Exception as e:
        print(f"Error generating Bagrut Q&A: {e}")
        return {"error": str(e)}


def save_bagrut_qa(question, answer):
    """
    Saves each question and answer in the global list.
    """
    global bagrut_qa_list
    bagrut_qa_list.append({"question": question, "answer": answer})
