from functions.book import get_possible_chapter_list


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


def build_plot_points_prompt(book_name, chapter_name, page_content):
    """
    Builds a prompt for generating plot points of a book chapter.

    Parameters:
    book_name (str): The name of the book.
    chapter_name (str): The name of the chapter.
    page_content (str): The content of the current page.

    Returns:
    str: The constructed prompt for the language model.
    """
    prompt = (f"Generate detailed plot points for the book '{book_name}', Chapter '{chapter_name}' "
              f"based on the following content:\n\n"
              f"{page_content}\n\n"
              "Include the following categories: death and tragic events, decisions, conflicts, character development, "
              "symbolism and imagery, foreshadowing, setting description, and a brief chapter summary.")
    return prompt


def build_bagrut_questions_prompt(book_name, chapter_name, plot_point_data, bagrut_examples):
    prompt_lines = [
        f"Based on the detailed summary of '{book_name}', Chapter '{chapter_name}', ",
        "generate Bagrut-level educational questions. Use the following examples as a guide:\n"
    ]
    for example in bagrut_examples:
        prompt_lines.append(f"- {example['question']} (Type: {example['type']})\n")

    prompt_lines.append("\nFocus on character motivations, plot implications, thematic elements, ")
    prompt_lines.append("and any significant narrative techniques used in this chapter.\n")
    prompt_lines.append("Additionally, use the following plot points to guide the question generation:\n")
    for key, value in plot_point_data.items():
        prompt_lines.append(f"- {key.replace('_', ' ').title()}: {value}\n")

    return ''.join(prompt_lines)


def build_bagrut_answers_prompt(book_name, chapter_name, detailed_summary, questions):
    """
    Builds a prompt for generating Bagrut-level answers based on questions and a chapter summary.

    Parameters:
    book_name (str): The name of the book.
    chapter_name (str): The name of the chapter.
    detailed_summary (str): The detailed summary of the chapter.
    questions (str): The Bagrut-level questions generated previously.

    Returns:
    str: The constructed prompt for the language model to generate Bagrut-level answers.
    """
    prompt = (f"Based on the detailed summary of '{book_name}', Chapter '{chapter_name}', "
              "and the following Bagrut-level questions, generate detailed answers. "
              "Focus on character motivations, plot implications, thematic elements, "
              "and any significant narrative techniques used in this chapter.\n\n"
              f"Detailed Summary:\n{detailed_summary}\n\n"
              f"Questions:\n{questions}\n")
    return prompt
