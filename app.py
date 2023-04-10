import streamlit as st

# Set page title
st.set_page_config(page_title='My Streamlit App')

# Add a title
st.title('Welcome to my Streamlit app!')

# Add a text input box
user_input = st.text_input('Please enter your name:', '')

# Display a message using the user's input
if user_input:
    st.write(f'Hello, {user_input}!')
