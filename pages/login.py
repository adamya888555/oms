import os
import sys
# Append the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from auth.auth import login

st.set_page_config(page_title="Order Management System ", layout="centered")
st.title(" Order Management System ")

# Center the login form
with st.form(key="login_form"):
    st.subheader("Please enter your credentials")
    # username = st.text_input("Username", placeholder="Enter your username")
    # password = st.text_input("Password", type="password", placeholder="Enter your password")
    username = "Adamya"
    password = "admin123"
    submit_button = st.form_submit_button("Login")

    if submit_button:
        if username=="Adamya" and password=="admin123":
            role = login(username, password)
            if role:
                st.session_state["role"] = role
                st.session_state["username"] = username
                st.success(f"Welcome, {username}! Redirecting to Order Status Checker...")
                st.switch_page("pages/MainApp.py")
            else:
                st.error("Invalid username or password. Please try again.")
        else:
            st.error("Please enter both username and password.")

if "role" in st.session_state:
    st.info(f"You are logged in as {st.session_state['username']} ({st.session_state['role']})")