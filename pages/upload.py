import streamlit as st

st.set_page_config(page_title='2nd Page', initial_sidebar_state="collapsed")

st.title('Welcome to my Streamlit app!')
st.success('Successfully logged in!')

model_file_path = st.file_uploader(label = 'Upload the Model')

rows = st.columns(2)
train_dataset_file_path = rows[0].file_uploader(label = 'Upload the Reference Data')
test_dataset_file_path = rows[1].file_uploader(label = 'Upload the Exploration Data')