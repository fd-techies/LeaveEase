import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from datetime import datetime
from database import leaveApplications

def createPage(username: str):

    #Page Layout
    selected = option_menu(
        menu_title=None,
        options=["Vacation Leave Application", "Misc Leave Application", "Leave Deletion", "Overseas Checker"],
        icons=["calendar-event", "calendar-event", "calendar-x", "calendar-check"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    #Welcome the user
    st.markdown("Welcome **:blue[{}]**".format(username))

    #Page option selection
    if selected == "Vacation Leave Application":
        applications = leaveApplications(local=True)
        with st.form("vacation_leave_application", clear_on_submit=True):
            st.date_input(label = "Select your vacation for next year", value = (datetime.now(), datetime.now()),key="vacationLeave")
            applyLeave = st.form_submit_button("Apply Leave")
            if applyLeave:
                leave_dates = st.session_state["vacationLeave"]
                start = leave_dates[0]
                end = leave_dates[1]
                message, success = applications.addUserApplication(name=username, start = start, end = end)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        #Show applied leaves
        leave_df = pd.DataFrame(applications.getUserApplication(username),columns=['name','type','start','end'])
        leave_df['selectbox'] = [False]*len(leave_df)
        # st.dataframe(leave_df, hide_index=True, use_container_width=True)
        st.data_editor(leave_df, column_config={"selectbox": st.column_config.CheckboxColumn("Delete", help="Check to delete", default=False)}, hide_index=True, use_container_width=True)

    return True