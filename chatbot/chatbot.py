import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def ask_chatbot(prompt):
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
        # Save the raw response to a JSON file
        with open("chatbot/output/raw_response.json", "w") as f:
            json.dump(response.json(), f, indent=4)
        
        # Extract the text part from the response
        text_parts = [part['text'] for part in response.json()['candidates'][0]['content']['parts']]
        
        # Save the text part to a separate file
        with open("chatbot/output/text_output.txt", "w") as f:
            f.write("\n\n".join(text_parts))
        
        return "Result saved to output/raw_response.json and output/text_output.txt"
    else:
        # Return the error
        return {"error": response.text}

# Read the contents of the file as the prompt
with open("chatbot/input/input_prompt.txt", "r") as file:
    prompt = file.read()

# Example usage
result = ask_chatbot(prompt)
print(result)
