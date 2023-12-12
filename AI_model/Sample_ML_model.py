#Required Libraries
import pandas as pd
import numpy as np 

file_path = "D:\AI_Project\Book_Recommendation_using_Artificial_Intelligence\AI_model\storage\data_genre.csv"

#Read the Dataset
books = pd.read_csv(file_path)

# Remove duplicate rows
books = books.drop_duplicates()

from sklearn.feature_extraction.text import TfidfVectorizer
tfv = TfidfVectorizer(min_df=3, max_features=None,
                    strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
                     ngram_range=(1,3),
                     stop_words = 'english')
    
#Filling NaN with empty string
books['summary'] = books['summary'].fillna('')

tfv_matrix = tfv.fit_transform(books['summary'])

from sklearn.metrics.pairwise import sigmoid_kernel

#compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

indices = pd.Series(books.index, index=books['title']).drop_duplicates()

    
def give_rec_based_on_genre(user_genre, sig=sig):
    # Get indices of books related to the user's specified genre
    genre_indices = books[books['genre'].str.contains(user_genre, case=False)].index
    
    # Calculate the average similarity scores for books in the specified genre
    avg_scores = np.mean(sig[genre_indices], axis=0)
    
    # Enumerate and sort the books based on the average similarity scores
    sorted_books = sorted(list(enumerate(avg_scores)), key=lambda x: x[1], reverse=True)
    
    # Get the top 5 recommendations
    top_recommendations = sorted_books[:5]
    
    # Books indices
    books_indices = [i[0] for i in top_recommendations]
    
    # Recommended Books
    return books['title'].iloc[books_indices]

# # Example usage:
# user_genre = input("Enter your preferred genre or interest: ")
# recommended_books = give_rec_based_on_genre(user_genre)

# print("Recommended Books:")
# print(recommended_books)

    
# def give_rec_based_on_title(user_title, sig=sig):
#     # Get indices of books related to the user's specified genre
#     title_indices = books[books['title'].str.contains(user_title, case=False)].index
    
#     # Calculate the average similarity scores for books in the specified genre
#     avg_scores = np.mean(sig[title_indices], axis=0)
    
#     # Enumerate and sort the books based on the average similarity scores
#     sorted_books = sorted(list(enumerate(avg_scores)), key=lambda x: x[1], reverse=True)
    
#     # Get the top 5 recommendations
#     top_recommendations = sorted_books[1:6]
    
#     # Books indices
#     books_indices = [i[0] for i in top_recommendations]
    
#     # Recommended Books
#     return books['title'].iloc[books_indices]

# # Example usage:
# user_genre = input("Enter your preferred title: ")
# recommended_books = give_rec_based_on_title(user_genre)

# print("Recommended Books:")
# print(recommended_books)
import joblib

# Save the model to a file
joblib.dump(sig, 'recommendation_model.joblib')
