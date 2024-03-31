import os
import json
import requests
from dotenv import load_dotenv
import pdfplumber

# Load environment variables from .env file
load_dotenv()

def get_book_chapter(book_name, chapter: int):
    pdf_path = os.path.join("static", "books", f"{book_name}.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[chapter - 1]
        return first_page.extract_text()

def build_prompt(book_name, chapter_name, page_number, page_content, next_page_content, previous_summaries):
    previous_summary_text = "\n\n".join(previous_summaries)
    prompt = (f"Summary of {book_name}, Chapter '{chapter_name}', Page {page_number}:\n\n{page_content}\n\n"
              f"Continued on next page:\n{next_page_content}\n\nPrevious summaries:\n{previous_summary_text}\n\n"
              "Please generate a detailed summary for this page, focusing on key plot points, "
              "character developments, and story-driven actions. Include any significant decisions made by characters, "
              "conflicts, emotional moments, and elements of foreshadowing or symbolism.")
    return prompt

def build_qa_prompt(book_name, chapter_name, detailed_summary):
    prompt = (f"Based on the detailed summary of '{book_name}', Chapter '{chapter_name}', "
              "generate a set of educational questions and their corresponding answers. Focus on character motivations, "
              "plot implications, thematic elements, and any significant narrative techniques used in this chapter.\n\n"
              f"Detailed Summary:\n{detailed_summary}\n")
    return prompt

def generate_summary(prompt):
    google_api_key = os.getenv('GOOGLE_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    params = {"key": google_api_key}
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code == 200:
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        return summary
    else:
        return {"error": response.text}

def generate_chapter_summaries_and_qa(book_name, book_chapters, chapter_names):
    chapter_summaries = []
    previous_summaries = []
    questions_and_answers = []
    
    for i, chapter_number in enumerate(book_chapters):
        chapter_content = get_book_chapter(book_name, chapter_number)
        next_chapter_content = get_book_chapter(book_name, book_chapters[i + 1]) if i < len(book_chapters) - 1 else ""
        detailed_summary_prompt = build_prompt(book_name, chapter_names[i], chapter_number, chapter_content, next_chapter_content, previous_summaries)
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
book_name = "master_margarita"
book_chapters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
chapter_names = ["Never Talk to Strangers", "Pontius Pilate", "The Seventh Proof", "The Pursuit", "The Affair at Griboyedov",
                 "Schizophrenia", "The Haunted Flat", "A Duel between Professor and Poet", "Koroviev's Tricks", "News from Yalta"]
summary_file_path, qa_file_path = generate_chapter_summaries_and_qa(book_name, book_chapters, chapter_names)
print("Summaries saved to:", summary_file_path)
print("Q&A saved to:", qa_file_path)

