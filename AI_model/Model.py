# Adding Required Libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from sklearn.pipeline import Pipeline
from scipy.sparse import save_npz

# Read the Dataset
processed_file_path = "D:\AI_Project\Book_Recommendation_using_Artificial_Intelligence\AI_model\storage\preprocessed.csv"
books = pd.read_csv(processed_file_path)

# Drop unnecessary data
books_cleaned = books.drop(columns=['ISBN', 'PublishYear', 'Publisher', 'BookSeriesInfo'])

# Remove duplicate rows
books_cleaned = books_cleaned.drop_duplicates()

# TF-IDF Vectorization
tfv = TfidfVectorizer(min_df=3, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 3),
                      stop_words='english')

# Filling NaN with empty string
books_cleaned['Description'] = books_cleaned['Description'].fillna('')
tfv_matrix = tfv.fit_transform(books_cleaned['Description'])

# Save tfv_matrix to a file
save_npz("tfv_matrix.npz", tfv_matrix)

# Create a pipeline with TF-IDF vectorizer
model = Pipeline([
    ('tfidf', tfv)
])

# Fit the pipeline with your data
model.fit(books_cleaned['Description'])

# Save the entire model using joblib
model_filename = "book_recommendation_model.joblib"
joblib.dump(model, model_filename)


