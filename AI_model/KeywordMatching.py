import re
from textblob import TextBlob,Word

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
    # file_path = "storage/book_genres.txt"

    # # Read genres from the text file
    # with open(file_path, "r") as file:
    #     genre_keywords = [line.strip() for line in file]

    genre_keywords = ['Fantasy', 'Science', 'Crime', 'History', 'Horror', 'Thriller', 'Psychology', 'Romance', 'Sports', 'Travel']

    title_keywords = ["The Great Gatsby", "Harry Potter", "To Kill a Mockingbird"]

    # # Correct the spelling mistake
    # ex = TextBlob(input_text)
    # corrected_words = []

    # for word in ex.words:
    #     corrected_words.append(word.correct())

    corrected_text = process_sentence(input_text)
    # print(corrected_text)

    # Check for Genre Keywords
    for keyword in genre_keywords:
        if re.search(keyword, corrected_text, re.IGNORECASE):
            return "Genre", keyword

    # Check for Title Keywords
    for keyword in title_keywords:
        if re.search(keyword, corrected_text, re.IGNORECASE):
            return "Title", keyword
    
    # If no keywords match, consider it a General question
    return "General", None

# Example Usage:
# user_input = "i like romance?"
# classification = classify_user_input(user_input)
# print(f"Classification: {classification}")

# # Number of user inputs you want to classify
# num_inputs = 3  # You can change this to the desired number of inputs

# # # Iterate for the specified number of inputs
# # for _ in range(num_inputs):
# #     user_input = input("Enter user input: ")
# #     classification = classify_user_input(user_input)
# #     print(f"User Input: {user_input}, Classification: {classification}")

# for _ in range(num_inputs):
#     user_input = input("Enter user input: ")
#     classification, keyword = classify_user_input(user_input)
#     print(f"User Input: {user_input}, Classification: {classification}, Matching Keyword: {keyword}")
