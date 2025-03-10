import streamlit as st

from api.api import create_user

import asyncio


def registration_page():
    st.title("User Registration Page")
    with st.form(key="registration_form"):
        username = st.text_input("Username")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        city = st.text_input("City")
        country = st.text_input("Country")
        password = st.text_input("Password", type="password")

        submit_button = st.form_submit_button("Register")

        if submit_button:
            if not all([username, first_name, last_name, email, phone, city, country, password]):
                st.error("Please fill in all fields.")
                return

            user_request = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "city": city,
                "country": country,
                "password": password,
            }

            # API Call
            try:
                user = create_user(user_request)
                st.success(f"User {user['username']} registered successfully!")
            except ValueError as e:
                st.error(f"Registration error: {e}")