import streamlit as st
from database.db import supabase


# ---------------- SIGNUP ---------------- #

def signup_user(email, password):

    try:

        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        return response

    except Exception as e:
        st.error(e)


# ---------------- LOGIN ---------------- #

def login_user(email, password):

    try:

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return response

    except Exception as e:
        st.error(e)


# ---------------- GOOGLE LOGIN ---------------- #

def google_login():

    try:

        response = supabase.auth.sign_in_with_oauth({
            "provider": "google"
        })

        return response.url

    except Exception as e:
        st.error(e)


# ---------------- LOGOUT ---------------- #

def logout_user():

    supabase.auth.sign_out()