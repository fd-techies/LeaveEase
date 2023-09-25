import streamlit as st
from database import Users, publicHolidays, leaveApplications
from datetime import datetime, date  # Core Python Module
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from views import vacation_leave



def main(local_toggle: bool):
    # -------------- SETTINGS --------------
    page_title = "LeaveEase"
    page_icon = ":luggage:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    layout = "wide"
    # --------------------------------------

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)
    menu = ["Login","Sign Up"]
    choice = st.sidebar.selectbox("Menu",menu)

    # --- NAVIGATION MENU ---
    

    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type="password")
        login = st.sidebar.button("Login")
        if "load_state" not in st.session_state:
            st.session_state.load_state = False
        if login or st.session_state.load_state:
            st.session_state.load_state = True
            users = Users(local=local_toggle)
            message, success = users.matchUsernamePassword(username,password)
            if success:
                vacation_leave.createPage(username)
                
                # st.sidebar.success(message)

            else:
                st.sidebar.error(message)

    elif choice == "Sign Up":
        with st.form("sign_up", clear_on_submit=True):
            st.subheader("Create New Account")
            st.selectbox("Select Team", ["A","B","C","D"], key="team")
            st.selectbox("Select Division", ["OC","FM","MCS","VCS","G","J","L"], key="division")
            st.text_input("New Username", key="username")
            st.text_input("New Password",type="password", key="password")
            st.number_input("Input number of vacation leave left", step=0.5, key="vacation")
            phList = publicHolidays(local=local_toggle).getAllPublicHolidayName()[:-1]
            st.multiselect("Please select Off in Lieu", phList, key="offInLieu")
            addUser = st.form_submit_button("Register")
            if addUser:
                users = Users(local=local_toggle)
                newTeam = str(st.session_state["team"])
                newDivision = str(st.session_state["division"])
                newUsername = str(st.session_state["username"])
                newPassword = str(st.session_state["password"])
                vacationLeave = int(st.session_state["vacation"])
                offInLieu = st.session_state["offInLieu"]
                message, success = users.addUser(team = newTeam, division = newDivision, username = newUsername, password = newPassword, noOfVacationLeave = vacationLeave, noOfOffInLieu = offInLieu)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    return True
    



if __name__=="__main__":
    main(local_toggle=True)
