from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Prompt('{self.prompt_text}', '{self.response_text}')"

def save_prompt(prompt_text, response_text):
    """
    Save a prompt and its response to the database.

    Parameters:
    prompt_text (str): The prompt text sent to the chatbot.
    response_text (str): The response text received from the chatbot.
    """
    prompt = Prompt(prompt_text=prompt_text, response_text=response_text)
    db.session.add(prompt)
    db.session.commit()

def get_all_prompts():
    """
    Retrieve all saved prompts and their responses from the database.

    Returns:
    list: A list of Prompt objects.
    """
    return Prompt.query.all()