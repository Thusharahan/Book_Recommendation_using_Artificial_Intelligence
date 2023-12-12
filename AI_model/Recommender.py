# Required Libraries
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz

# Load tfv_matrix from the file
tfv_matrix = load_npz("tfv_matrix.npz")

# Load the saved model
model_filename = "book_recommendation_model.joblib"
loaded_model = joblib.load(model_filename)

# Read the dataset (make sure to use the same preprocessing steps as in your original code)
books_cleaned_file_path = r"D:\AI_Project\Book_Recommendation_using_Artificial_Intelligence\AI_model\storage\books_cleaned.csv"

# Load books_cleaned from the CSV file in another program
books_cleaned = pd.read_csv(books_cleaned_file_path)

def recommended_books(user_input):

    # Transform the user input using the loaded model
    user_input_vectorized = loaded_model.transform([user_input])

    # Calculate cosine similarity between user input and all books
    cosine_similarity_scores = cosine_similarity(user_input_vectorized, tfv_matrix).flatten()

    # Get indices of top 5 similar books
    top_recommendations_indices = cosine_similarity_scores.argsort()[:-6:-1]


    # Retrieve and print the top 5 recommended books
    recommended_books = books_cleaned.iloc[top_recommendations_indices]
    recommended_books = recommended_books[['Name', 'Authors']]

    # recommended_books['Authors'] = recommended_books['Authors'].astype(str)
    
    # recommended_books['Authors'] = recommended_books['Authors'].replace("_", "")

    # # Capitalize the first word of each column
    # recommended_books['Name'] = recommended_books['Name'].str.capitalize()
    # recommended_books['Authors'] = recommended_books['Authors'].str.capitalize()
    # Remove underscores and capitalize each word in 'Name' and 'Authors' columns

    # recommended_books['Name'] = recommended_books['Name'].str.split(' ').apply(lambda x: ' '.join(map(str.capitalize, x)))
    recommended_books['Name'] = recommended_books['Name'].str.split('(').apply(lambda x: '('.join(map(str.capitalize, x)))
    # recommended_books['Authors'] = recommended_books['Authors'].str.replace("_", "").str.title()
    recommended_books['Authors'] = recommended_books['Authors'].str.split('_').apply(lambda x: ' '.join(map(str.capitalize, x)))

    return recommended_books

# # print(recommended_books("romance").shape)
# response = recommended_books("roamce")

# # # Create a formatted string for each book
# # formatted_books = ["- Name: {}\n  Author: {}\n  Description: {}".format(book["Name"], book["Authors"], book["Description"]) for book in response]

# # # Join the formatted strings with newline characters to create the final string
# # response_str = "\n".join(formatted_books)

# # # Print or use response_str as needed
# # print(response_str)

# # response['Authors'] = response['Authors'].replace("_", "")
# #     # Capitalize the first word of each column
# # response['Name'] = response['Name'].str.capitalize()
# # response['Authors'] = response['Authors'].str.capitalize()

# # Create a formatted string for each book
# formatted_books = ["- Name: {}\n  Author: {}".format(row['Name'], row['Authors']) for index, row in response.iterrows()]

# # Join the formatted strings with newline characters to create the final string
# response_str = "\n".join(formatted_books)

# # Print or use response_str as needed
# print(response_str)

