import re
from textblob import TextBlob

def process_sentence(sentence):
    # Correct the spelling mistake
    ex = TextBlob(sentence)
    corrected_words = []

    for word in ex.words:
        corrected_words.append(word.correct())
    
    # Form a new sentence from the corrected words
    new_sentence = ' '.join(corrected_words)

    return new_sentence

def classify_user_input(input_text):
    # Define Keywords
    # Specify the file path where the genres are stored
    file_path_genre = "storage/genres.txt"

    # Read genres from the text file
    with open(file_path_genre, "r") as file:
        genre_keywords = [line.strip() for line in file]

    file_path_notgenre = "storage/not_in_genre.txt"

    # Read genres from the text file
    with open(file_path_notgenre, "r") as file:
        notgenre_keywords = [line.strip() for line in file]

    corrected_text = process_sentence(input_text)
    # print(corrected_text)

    # Check for Genre Keywords
    for keyword in genre_keywords:
        if re.search(keyword, corrected_text, re.IGNORECASE):
            return "Genre", keyword
    
    # Check for Genre Keywords
    for keyword in notgenre_keywords:
        if re.search(keyword, corrected_text, re.IGNORECASE):
            return "NGenre", keyword
    
    # If no keywords match, consider it a General question
    return "General", None