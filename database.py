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
        

    def addUser(self, username: str, password: str, noOfVacationLeave: int, noOfOffInLieu: list):
        #     """Returns the report on a successful creation, otherwise raises an error"""
        db = self.deta.Base("users")
        return db.put({"username": username, "password": password, "noOfVacationLeave": noOfVacationLeave, "noOfOffInLieu": noOfOffInLieu})
    
    def getAllUsers(self):
        db = self.deta.Base("users")
        return db.fetch().items
    
    def matchUsernamePassword(self, username: str, password: str):
        db = self.deta.Base("users")
        all_users = db.fetch().items
        message = "Logged in as {}".format(username)
        success = True
        try:
            user = [user for user in all_users if user['username']==username][0]
        except:
            message = "Please Sign Up first"
            success = False
            return message, success
        if user["password"]!=password:
            message = "Wrong Password!"
            success = False
        return message, success

    
if __name__=="__main__":
    users = Users(local=True)
    print(users.getAllUsers())