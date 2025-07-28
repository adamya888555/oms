import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from datetime import datetime
from workflows.order_flow import OrderWorkflow
from data.storage import OrderStorage
import re

st.set_page_config(page_title="Order Status Checker", layout="centered")
st.title("Order Management System")

# Initialize storage and workflow
if "workflow" not in st.session_state:
    st.session_state["workflow"] = OrderWorkflow(OrderStorage())

# Check if user is logged in
if "role" not in st.session_state:
    st.warning("Please log in first via the Login page.")
    st.switch_page("login.py")
    st.stop()

# Sidebar with user info and logout
st.sidebar.write(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
if st.sidebar.button("Logout"):
    for key in ["role", "username", "messages", "workflow"]:
        if key in st.session_state:
            del st.session_state[key]
    st.switch_page("login.py")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle user input
user_input = st.chat_input("Enter your message (e.g., 'Check status of order 21-39832 Mobile Recharge' or 'Hi, how's it going?')")
if user_input:
    # Append user message to chat history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })

    # Process input using OrderWorkflow
    response, order_data = st.session_state["workflow"].run(user_input, st.session_state["role"])

    # Append assistant response to chat history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({
        "role": "assistant",
        "content": {"response": response, "order_data": order_data},
        "timestamp": timestamp
    })


# Display chat messages
# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.write(msg["content"])
            
        elif msg["role"] == "assistant":
            content = msg["content"]
            
            if isinstance(content, dict) and content.get("order_data"):
                # Intent = order status (order_data present)
                order_data = content["order_data"]
                st.write("Order Status:")

                system_statuses = order_data.get("system_statuses")
                if system_statuses:
                    st.table([
                        {"System": system.capitalize(), "Status": status.capitalize()}
                        for system, status in system_statuses.items()
                    ])

                response_text = content["response"]

                # Split to insert dashed line before Overall Status
                parts = response_text.split("\nOverall Status:")
                if len(parts) == 2:
                    before_status = parts[0].rstrip()
                    after_status = parts[1].lstrip()
                    new_response = f"{before_status}\n--------------------\n"
                else:
                    new_response = response_text
                    after_status = ""

                overall_status_line = ""
                detailed_status_text = ""
                if after_status:
                    lines = after_status.splitlines()
                    if lines:
                        overall_status_line = lines[0].strip()
                        detailed_status_text = "\n".join(lines[1:]).strip()

                # Show parts before Overall Status + dashed line
                st.text(new_response)

                # Show Overall Status box ONLY here (order status intent)
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #333333;
                        border-radius: 5px;
                        background-color: #f0f0f0;
                        color: #222222;
                        padding: 10px 15px;
                        font-weight: bold;
                        width: fit-content;
                        font-size: 1.1em;
                        margin-bottom: 10px;
                    ">
                        Overall Status: {overall_status_line}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.text("")  # gap

                # Show detailed system statuses text below the box
                if detailed_status_text:
                    st.text(detailed_status_text)

            else:
                # For small talk or other intents: no order_data
                # Just display the assistant's response text as-is, no Overall Status box
                st.text(content["response"])

        st.caption(msg["timestamp"])
