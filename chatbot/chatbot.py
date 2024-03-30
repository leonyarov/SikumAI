import os
import json
import requests
from dotenv import load_dotenv
import pdfplumber

# Load environment variables from .env file
load_dotenv()

def get_book_chapter(book_name, chapter: int):
    # Construct the path to the PDF file dynamically based on the book name
    pdf_path = os.path.join("static", "books", f"{book_name}.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[chapter - 1]  # Adjusted to 0-based index
        return first_page.extract_text()

def build_prompt(book_name, chapter_name, page_number, page_content, next_page_content, previous_summaries):
    # Build a prompt for the chatbot using the page content, chapter name, and previous summaries
    previous_summary_text = "\n\n".join(previous_summaries)
    prompt = f"Summary of {book_name}, Chapter '{chapter_name}', Page {page_number}:\n\n{page_content}\n\nContinued on next page:\n{next_page_content}\n\nPrevious summaries:\n{previous_summary_text}\n\nPlease generate a summary for this page."
    return prompt

def generate_summary(prompt):
    # Access the environment variables
    google_api_key = os.getenv('GOOGLE_API_KEY')
    
    # Define the URL
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    # Define the request payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    # Set the headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key to parameters
    params = {
        "key": google_api_key
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, params=params, json=payload)
    
    # Check the response status
    if response.status_code == 200:
        # Extract and return the summary from the response
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        return summary
    else:
        # Return the error
        return {"error": response.text}

def generate_chapter_summaries(book_name, book_chapters, chapter_names):
    chapter_summaries = []
    previous_summaries = []  # Store previous summaries
    for i, chapter_number in enumerate(book_chapters):
        chapter_content = get_book_chapter(book_name, chapter_number)
        next_chapter_number = book_chapters[i + 1] if i < len(book_chapters) - 1 else None
        next_chapter_content = get_book_chapter(book_name, next_chapter_number) if next_chapter_number else ""
        prompt = build_prompt(book_name, chapter_names[i], chapter_number, chapter_content, next_chapter_content, previous_summaries)
        summary = generate_summary(prompt)
        chapter_summaries.append(summary)
        previous_summaries.append(summary)  # Add the current summary to the list of previous summaries
    
    # Construct output file name
    output_file_name = f"{book_name}_page{'_'.join(map(str, book_chapters))}_summaries.txt"
    output_file_path = os.path.join("chatbot", "output", output_file_name)
    
    # Write summaries to the output file
    with open(output_file_path, "w") as output_file:
        for i, summary in enumerate(chapter_summaries):
            output_file.write(f"Summary of Chapter {book_chapters[i]} - {chapter_names[i]}:\n")
            output_file.write(summary + "\n\n")
    
    return output_file_path

# Example usage
book_name = "master_margarita"  # Example book name
book_chapters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
chapter_names = ["Never Talk to Strangers", "Pontius Pilate", "The Seventh Proof", "The Pursuit", "The Affair at Griboyedov",
                 "Schizophrenia", "The Haunted Flat", "A Duel between Professor and Poet", "Koroviev's Tricks", "News from Yalta"]  # Assuming you have chapter names in a list
output_file_path = generate_chapter_summaries(book_name, book_chapters, chapter_names)
print("Summaries saved to:", output_file_path)
