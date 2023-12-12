import streamlit as st
from rag_with_palm import RAGPaLMQuery
import KeywordMatching as kw
import pandas as pd
import Recommender as rec

# Instantiate the class
rag_palm_query_instance = RAGPaLMQuery()

st.title(f"**Book Recommending Assistant**📚")  

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Need any book recommendation? Drop your questions here!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    classification, keyword = kw.classify_user_input(prompt)
    
    # Initialize combined_response
    combined_response = ""  

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
            
            response = rec.recommended_books(keyword)

            formatted_books = ["- **{}** \n  Author: {}".format(row['Name'], row['Authors']) for index, row in response.iterrows()]

            # Join the formatted strings with newline characters to create the final string
            response_str = "\n".join(formatted_books)

            combined_response = str(model_response) + "\n\n" + caption + "\n" + response_str

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(combined_response)

            # Add assistant responses to chat history
            st.session_state.messages.append({"role": "assistant", "content": combined_response})
