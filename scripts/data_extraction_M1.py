"""
Module: data_extraction_M1
Team Member 1: Parsing Module

This module provides tools for extracting structured answer sequences
from raw quiz response text files, and for writing these sequences to
clean, standardised output files.

Functions
---------
extract_answers_sequence(file_path):
    Parse a raw respondent file and return a list of 100 integers
    representing selected answers (1–4) or 0 for unanswered.

write_answers_sequence(answers, n, destination_path):
    Save a list of 100 integers to a text file named
    'answers_list_respondent_n.txt' inside the destination folder.
"""

import os


def extract_answers_sequence(file_path):
    """
    Extract the sequence of 100 answers from a raw quiz response file.

    Parameters
    ----------
    file_path : str
        Path to the raw respondent file (e.g., 'data/a1.txt').

    Returns
    -------
    list of int
        A list of length 100 where each element is:
        - 1, 2, 3, or 4 if that option was selected,
        - 0 if the question was left unanswered.

    Raises
    ------
    FileNotFoundError
        If the file_path does not exist.
    ValueError
        If fewer or more than 100 questions are detected.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    answers = []
    current_question_answers = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

           
            if stripped.startswith("["):
                
            
              
                if "[x]" in stripped.lower():
                    current_question_answers.append(1)
                elif "[ ]" in stripped:
                    current_question_answers.append(0)

              
                if len(current_question_answers) == 4:
                    if 1 in current_question_answers:
                      
                        answers.append(current_question_answers.index(1) + 1)
                    else:
                        answers.append(0)  
                    current_question_answers = []

    if len(answers) != 100:
        raise ValueError(
            f"Expected 100 questions, but extracted {len(answers)} from {file_path}"
        )

    return answers


def write_answers_sequence(answers, n, destination_path):
    """
    Write a list of 100 integers to a clean output file.

    Parameters
    ----------
    answers : list of int
        A list of 100 integers representing the respondent's answers.

    n : int
        Respondent ID number (e.g., 1, 2, 3...).

    destination_path : str
        Folder where the output file should be saved.

    Returns
    -------
    None
        Writes a file named 'answers_list_respondent_n.txt'.

    Raises
    ------
    ValueError
        If the answers list is not length 100.
    """
    if len(answers) != 100:
        raise ValueError("Answer list must contain exactly 100 integers.")

    os.makedirs(destination_path, exist_ok=True)

    output_file = os.path.join(
        destination_path, f"answers_list_respondent_{n}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        for a in answers:
            f.write(str(a) + "\n")
