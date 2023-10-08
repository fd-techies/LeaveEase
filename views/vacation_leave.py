import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from datetime import datetime, timedelta
from database import leaveApplications


def createPage(username: str, local_toggle: bool):

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
        applications = leaveApplications(local=local_toggle)
        #Show applied leaves
        leave_dict = applications.getUserApplication(username)
        full_leave_df = pd.DataFrame(leave_dict, columns=['key', 'type', 'start', 'end'])
        leave_keys = full_leave_df['key'].copy().to_list()
        leave_df = full_leave_df[['type','start','end']].copy()
        leave_df['start'] = pd.to_datetime(leave_df['start'])
        leave_df['end'] = pd.to_datetime(leave_df['end'])
        config={
            "type": st.column_config.SelectboxColumn(label = "Leave Type", options = ["Vacation Leave", "OIL", "MC"]),
            "start": st.column_config.DateColumn(label = "Leave Start"),
            "end": st.column_config.DateColumn(label = "Leave End"),
        }
        editted_leave = st.data_editor(leave_df, num_rows= "dynamic", use_container_width=True, column_config = config)
        editted_leave = editted_leave.to_dict('records')
        applyLeave = st.button("Save Leave")
        leave_calendar_list = []
        for leave_applied in editted_leave:
            leave_calendar_list.append({"title": leave_applied['type'], "start": str(leave_applied['start'].date()), "end": str(leave_applied['end'].date() + timedelta(days=1))})
        success=True
        message = "Leave applied successfully"
        if applyLeave:
            new_calendar_list = []
            for key in leave_keys:
                applications.deleteKeyApplication(key)
            for leave_applied in editted_leave:
                message, success = applications.addUserApplication(name=username, start = leave_applied['start'], end = leave_applied['end'], type= leave_applied['type'])
                if not success:
                    st.error(message)
                    break
                else:
                    new_calendar_list.append({"title": leave_applied['type'], "start": str(leave_applied['start'].date()), "end": str(leave_applied['end'].date() + timedelta(days=1))})
            if success:
                st.success(message)
            return new_calendar_list
        return leave_calendar_list