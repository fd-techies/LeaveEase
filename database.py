import os

import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from dotenv import load_dotenv


# Load the environment variables
# load_dotenv(".env")
# DETA_KEY = os.getenv("DETA_KEY")
DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("user_leave_period")

def insert_period(name: str, start_date: str, end_date: str):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": name, "start_date": start_date, "end_date": end_date})

if __name__=="__main__":
    insert_period("Elwin","121223","131223")