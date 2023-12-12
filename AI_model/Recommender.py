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

# Read the dataset
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

    recommended_books['Name'] = recommended_books['Name'].str.split('(').apply(lambda x: '('.join(map(str.capitalize, x)))
    recommended_books['Authors'] = recommended_books['Authors'].str.split('_').apply(lambda x: ' '.join(map(str.capitalize, x)))

    return recommended_books

