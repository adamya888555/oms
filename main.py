
import os
import sys
# Append the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st

st.set_page_config(page_title="Order Management System", initial_sidebar_state="expanded")
st.switch_page("pages/login.py")