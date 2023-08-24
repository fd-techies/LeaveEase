import streamlit as st
from database import Users
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu



def main():
    # -------------- SETTINGS --------------
    page_title = "LeaveEase"
    page_icon = ":luggage:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    layout = "wide"
    # --------------------------------------

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)
    menu = ["Login","Sign Up"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type="password")
        if st.sidebar.button("Login"):
            users = Users(local=False)
            message, success = users.matchUsernamePassword(username,password)
            if success:
                st.sidebar.success(message)
                # --- NAVIGATION MENU ---
                selected = option_menu(
                    menu_title=None,
                    options=["Leave Application", "Leave Deletion", "Overseas Checker"],
                    icons=["calendar-event", "calendar-x", "calendar-check"],  # https://icons.getbootstrap.com/
                    orientation="horizontal",
                )
                if selected == "Leave Application":
                    with st.form("leave_application", clear_on_submit=True):
                        col1, col2 = st.columns(2)
                        col1.date_input(label="Vacation Start Date", key="startDate")
                        col2.date_input(label="Vacation End Date", key="endDate")
                        submitted = st.form_submit_button("Apply Leave")
            else:
                st.sidebar.error(message)

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        st.text_input("New Username", key="username")
        st.text_input("New Password",type="password", key="password")
        st.number_input("Input number of vacation leave left", step=1, key="vacation")
        st.multiselect("Please select Off in Lieu", ["Hari Raya Haji","National Day"], key="offInLieu")
        addUser = st.button("Register")
        if addUser:
            users = Users(local=False)
            newUsername = str(st.session_state["username"])
            newPassword = str(st.session_state["password"])
            vacationLeave = int(st.session_state["vacation"])
            offInLieu = st.session_state["offInLieu"]
            try:
                users.addUser(username = newUsername, password = newPassword, noOfVacationLeave = vacationLeave, noOfOffInLieu = offInLieu)
                st.success("Account has been successfuly created")
            except:
                errorMessage = RuntimeError('This is an exception of type RuntimeError')
                st.exception(errorMessage)
    



if __name__=="__main__":
    main()
