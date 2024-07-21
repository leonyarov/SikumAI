# Lesson Plan builder and Chatbot invocation
from Chatbot.chatbot import execute_prompt, get_chapter_list
from database import LessonPlan
from functions.book import find_chapter
from functions.prompt_caching import save


def reading_comprehension(chapter):
    prompt = f"Choose short paragraph (5-7 lines) of text from the chapter.\n"
    result = execute_prompt(prompt + chapter)
    return result


def discussion_text(chapter):
    prompt = (f"Write 3 simple questions without answers that can be used to discuss the chapter.\n")
    result = execute_prompt(prompt + chapter)
    return result


def bagrut_questions(chapter):
    prompt = (f"Write 2 questions that can be used for a Bagrut exam.\n"
              f"Example: 'Characters in the play may feel towards each other empathy, compassion and a desire to help or behave hypocritically"
              f" and flatteringly, with hostility and ignoring and even malice. "
              f" What characterizes the relationships between characters in the play you studied? Explain and demonstrate your words with two of the relationships in the play. "
              f" In your answer, also write whether the characteristics of each of the relationships change throughout the play or do not change.'\n")
    result = execute_prompt(prompt + chapter)

    return result


def encourage_writing(chapter):
    prompt = (
        f"Write a question that can be used to give to a class of students to write an long answer to. involve one or two charecters: \n")
    # f"1. A letter to one of the characters [character name], "
    # f"2. Fictional possible conversation between two characters [character 1, character 2], "
    # f"3. Possible diary entry of the main character, "
    # f"4. Personal summary of [character], "
    result = execute_prompt(prompt + chapter)
    return result


def lesson_plan_prompt(chapter, book_name):
    chapter_list = get_chapter_list(book_name)
    chapter_text = find_chapter(chapter_name=chapter, book_name=book_name, chapter_list=chapter_list)
    rc = reading_comprehension(chapter_text)
    dt = discussion_text(chapter_text)
    bq = bagrut_questions(chapter_text)
    eq = encourage_writing(chapter_text)
    lp = LessonPlan(reading=rc, discussion=dt, bagrut=bq, writing=eq, book_name=book_name)
    save(lp)
    return lp
