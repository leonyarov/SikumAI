# Lesson Plan builder and chatbot invocation
from chatbot.chatbot import execute_prompt, get_chapter_list
from functions.book import find_chapter


def reading_comprehension():
    prompt = (f"Choose between 5 and 7 lines of text from the chapter.\n"
              f"format as follows: <reading>...</reading")
    return prompt


def discussion_text():
    prompt = (f"Write 3 simple questions without answers that can be used to discuss the chapter.\n"
              f"format as follows: wrap every question in <question></question> tags")
    return prompt


def bagrut_questions():
    prompt = (f"Write 2 questions that can be used for a Bagrut exam.\n"
              f"Example: 'Characters in the play may feel towards each other empathy, compassion and a desire to help or behave hypocritically"
              f" and flatteringly, with hostility and ignoring and even malice. "
              f" What characterizes the relationships between characters in the play you studied? Explain and demonstrate your words with two of the relationships in the play. "
              f" In your answer, also write whether the characteristics of each of the relationships change throughout the play or do not change.'\n"
              f"format as follows: wrap every question in <bagrut></bagrut> tags")
    return prompt


def encourage_writing():
    prompt = (f"choose one of the following examples to give in class (or think of something similar), augment it, dont write it, just choose:\n"
              f"A letter to one of the characters, "
              f"Fictional possible conversation between two characters, "
              f"Possible diary entry of the main character, "
              f"Personal summary, "
              f"format as follows: wrap it in <writing></writing> tags")
    return prompt


def lesson_plan_prompt(chapter, book_name):
    chapter_list = get_chapter_list(book_name)
    chapter_text = find_chapter(chapter_name=chapter, book_name=book_name, chapter_list=chapter_list)
    rc = reading_comprehension()
    dt = discussion_text()
    bq = bagrut_questions()
    eq = encourage_writing()
    prompt = "\n".join([rc, dt, bq, eq, chapter_text])
    return execute_prompt(prompt)



