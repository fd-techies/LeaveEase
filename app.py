#https://leaveease.streamlit.app/
import calendar  # Core Python Module
from datetime import datetime, date  # Core Python Module

import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

from database import Users

# -------------- SETTINGS --------------
page_title = "LeaveEase"
page_icon = ":luggage:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "wide"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Leave Application", "Leave Deletion", "Overseas Checker"],
    icons=["calendar-event", "calendar-x", "calendar-check"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# --- INPUT & SAVE PERIODS (Leave Application) ---
if selected == "Leave Application":
    with st.form("leave_application", clear_on_submit=True):
        st.write(list(st.secrets.keys())[1:])
        col1, col2 = st.columns(2)
        col1.text_input(label="Create new username", key="username")
        col2.text_input(label="Create new password (do not user personal sensitive password)", key="password")
        # col1.date_input("Start Date:", date(1970, 1, 1), min_value=date(1970, 1, 1),key="startdate")
        # col2.date_input("End Date:", date(1970, 1, 1), min_value=date(1970, 1, 1),key="enddate")

        submitted = st.form_submit_button("Save Data")
        if submitted:
            users = Users(local=False)
            newUsername = str(st.session_state["username"])
            newPassword = str(st.session_state["password"])
            try:
                users.addUser(username = newUsername, password = newPassword)
                st.success("Account has been successfuly created")
            except:
                errorMessage = RuntimeError('This is an exception of type RuntimeError')
                st.exception(errorMessage)

# --- INPUT & SAVE PERIODS (Leave Deletion) ---
if selected == "Leave Deletion":
    None

# --- INPUT & SAVE PERIODS (Overseas Checker) ---
if selected == "Overseas Checker":
    None