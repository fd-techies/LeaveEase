import os

import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from dotenv import load_dotenv

class Users:

    def __init__(self, local: bool):
        self.local = local
        if self.local:
           load_dotenv(".env")
           self.deta = Deta(os.getenv("DETA_KEY"))
        else:
           self.deta = Deta(st.secrets["DETA_KEY"])
        

    def addUser(self, username: str, numberOfLeave: int):
        #     """Returns the report on a successful creation, otherwise raises an error"""
        db = self.deta.Base("users")
        return db.put({"username": username, "numberOfLeave": numberOfLeave})
    
if __name__=="__main__":
    users = Users(local=True)
    users.addUser(username = "Elwin", numberOfLeave = 12)