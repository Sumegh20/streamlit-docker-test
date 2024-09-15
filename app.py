# import streamlit as st
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
# from firebase_admin import auth
# import json
# import requests
# from streamlit_extras.switch_page_button import switch_page
# import asyncio
# from httpx_oauth.clients.google import GoogleOAuth2

# cred = credentials.Certificate("streamlit-firebase-test-b879baa02ac8.json")
# # if st.session_state.get('is_initialize', default=True):
# #     firebase_admin.initialize_app(cred)
# #     st.session_state['is_initialize'] = False

# try:
#     firebase_admin.get_app()
# except ValueError as e:
#     firebase_admin.initialize_app(cred)


# # Set page title
# st.set_page_config(page_title='My Streamlit App', initial_sidebar_state="collapsed")

# # Add a title
# st.title('Welcome to my Streamlit app!')


# choice = st.selectbox('Login/Signup',['Login','Sign up'])
# email = st.text_input('Email Address')
# password = st.text_input('Password',type='password')


# if choice == 'Sign up':
#     username = st.text_input("Enter  your unique username")
    
#     if st.button('Create my account'):
#         user = auth.create_user(email = email, password = password, uid=username)
#         # user = sign_up_with_email_and_password(email=email,password=password,username=username)
        
#         st.success('Account created successfully!')
#         st.markdown('Please Login using your email and password')
#         st.balloons()
# else:
#     pass
#     if st.button('Login'):
#         try:
#             user = auth.get_user_by_email(email)
            
            
#             print(user.password)
#             st.success('Successfully logged in!')
#             switch_page("upload")
#         except Exception as e:
#             st.warning(f"login failed {e}")
#     # st.button('Login', on_click=f)
#     # if st.button('Forget'):
#     # forget()
#     # st.button('Forget',on_click=forget)

# const firebaseConfig = {
#   apiKey: "AIzaSyCq1CspDwSUI1YM7dW8WR4S_VmO3GieUYw",
#   authDomain: "streamlit-firebase-test.firebaseapp.com",
#   projectId: "streamlit-firebase-test",
#   storageBucket: "streamlit-firebase-test.appspot.com",
#   messagingSenderId: "563959437871",
#   appId: "1:563959437871:web:feeb006f76cd1a055cc4da",
#   measurementId: "G-VC70BNCE0X"
# }

import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
from streamlit_extras.switch_page_button import switch_page

# Initialize Firebase Admin SDK
cred = credentials.Certificate("streamlit-firebase-test-b879baa02ac8.json")

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

# Firebase REST API configuration
firebase_api_key = ""
firebase_auth_url = f""

# Set page title
st.set_page_config(page_title='My Streamlit App', initial_sidebar_state="collapsed")

# Add a title
st.title('Welcome to my Streamlit app!')

choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
email = st.text_input('Email Address')
password = st.text_input('Password', type='password') if choice != 'reset_password' else None

# Function to handle signup using Firebase Admin SDK
def sign_up_with_email_and_password(email, password, username):
    try:
        user = auth.create_user(email=email, password=password, uid=username)
        return user
    except Exception as e:
        st.error(f"Error creating account: {e}")

# Function to handle login using Firebase REST API
def login_with_email_and_password(email, password):
    try:
        login_url = f"{firebase_auth_url}:signInWithPassword?key={firebase_api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(login_url, json=payload)
        response_data = response.json()
        
        if 'idToken' in response_data:
            return response_data
        else:
            st.warning(f"Login failed: {response_data.get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during login: {e}")

# Function to handle password reset using Firebase REST API
def send_password_reset_email(email):
    try:
        reset_url = f"{firebase_auth_url}:sendOobCode?key={firebase_api_key}"
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }
        response = requests.post(reset_url, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            st.success(f"Password reset email sent to {email}.")
        else:
            st.warning(f"Password reset failed: {response_data.get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error sending password reset email: {e}")



# Signup Section
if choice == 'Sign up':
    username = st.text_input("Enter your unique username")
    
    if st.button('Create my account'):
        if email and password and username:
            user = sign_up_with_email_and_password(email=email, password=password, username=username)
            if user:
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            st.warning('Please fill out all fields.')

elif choice == "reset_password":
    if st.button('Reset Password'):
        if email:
            send_password_reset_email(email=email)
        else:
            st.warning('Please enter your email address.')

# Login Section
else:
    if st.button('Login'):
        if email and password:
            user_data = login_with_email_and_password(email=email, password=password)
            if user_data:
                st.success('Successfully logged in!')
                switch_page("upload")
        else:
            st.warning('Please enter your email and password.')
