import streamlit as st
from rag_with_palm import RAGPaLMQuery
import KeywordMatching as kw
import pandas as pd
# import Sample_ML_model as sml
# import NLPclassifier as nlp
import Recommender as rec
# import joblib

# # Load the pre-trained model
# model_path = 'recommendation_model.joblib'  # Adjust the path based on your actual file location
# sig_loaded = joblib.load(model_path)

# Instantiate the class
rag_palm_query_instance = RAGPaLMQuery()

st.title(f"**Book Recommender Assistant**📚")  # Add emojis and colors to the title
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Read the dataset (make sure to use the same preprocessing steps as in your original code)
books_cleaned_file_path = r"D:\AI_Project\Book_Recommendation_using_Artificial_Intelligence\AI_model\storage\books_cleaned.csv"

# Load books_cleaned from the CSV file in another program
book = pd.read_csv(books_cleaned_file_path)

# React to user input
if prompt := st.chat_input("Need any book recommendation? Drop your questions here!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    classification, keyword = kw.classify_user_input(prompt)
    
    # classification = nlp.classify_user_input_bert(prompt)
    combined_response = ""  # Initialize combined_response

    if classification == "General":
        model_response = rag_palm_query_instance.query_response(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(model_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": model_response})
    else:
        model_response = rag_palm_query_instance.query_response(prompt)
        if classification == "Genre":
            caption = "As you're interested in **{}**, I recommend you the following books:".format(keyword)
            # response = rec.give_rec_based_on_genre(keyword, sig=sig_loaded)
            response = rec.recommended_books(keyword)

            # # Convert the list to a string with each book as a bullet point
            # response_str = "\n".join("- {}".format(book) for book in response)

            # # Your existing code to convert the list to a string with each book as a bullet point
            # response_str = "\n".join("- {}".format(book['Name']) for book in response if isinstance(book, dict) and 'Name' in book)

            # # Additional code to print the desired format for each book
            # for book in response:
            #     response_str += "\n\n{} By {}\n{}".format(book['Authors'], book['Description'])
            # Create a formatted string for each book
            formatted_books = ["- **{}** \n  Author: {}".format(row['Name'], row['Authors']) for index, row in response.iterrows()]

            # Join the formatted strings with newline characters to create the final string
            response_str = "\n".join(formatted_books)

            combined_response = str(model_response) + "\n\n" + caption + "\n" + response_str

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(combined_response)

            # Add assistant responses to chat history
            st.session_state.messages.append({"role": "assistant", "content": combined_response})
