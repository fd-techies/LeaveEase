import os

import streamlit as st  # pip install streamlit
import pandas as pd
from deta import Deta  # pip install deta
from dotenv import load_dotenv
from datetime import datetime

class Users:

    def __init__(self, local: bool):
        self.local = local
        if self.local:
           load_dotenv(".env")
           self.deta = Deta(os.getenv("DETA_KEY"))
        else:
           self.deta = Deta(st.secrets["DETA_KEY"])
        

    def addUser(self, team: str, division: str, username: str, password: str, noOfVacationLeave: int, noOfOffInLieu: list):
        #     """For sign-up page: Add user into the Users database"""
        db = self.deta.Base("users")
        all_users = self.getAllUsernames()
        success = True
        if username in all_users:
            message = 'Username {} has already been used'.format(username)
            success = False
        else:
            db.put({"team": team, "division": division, "username": username, "password": password, "noOfVacationLeave": noOfVacationLeave, "noOfOffInLieu": noOfOffInLieu})
            message = "Account has been successfully created"
        return message, success
    
    def getAllUsers(self):
        #     """Get all the users with their leave balance details registered in LeaveEase"""
        db = self.deta.Base("users")
        return db.fetch().items
    
    def getAllUsernames(self):
        #     """Get all the usernames of the usernames of the users registered in LeaveEase"""
        db = self.deta.Base("users")
        all_users = db.fetch().items
        usernames = [user['username'] for user in all_users]
        return usernames
    
    def matchUsernamePassword(self, username: str, password: str):
        #     """For login page: Check if username and password matches whatever that is registered into LeaveEase"""
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
    
class leaveApplications:

    def __init__(self, local: bool):
        self.local = local
        if self.local:
           load_dotenv(".env")
           self.deta = Deta(os.getenv("DETA_KEY"))
        else:
           self.deta = Deta(st.secrets["DETA_KEY"])

    def getUserApplication(self, name: str):
        #     """Retireve all the leave applied by user"""
        db = self.deta.Base("leaveApplications")
        allApplications = db.fetch().items
        userApplications = []
        for application in allApplications:
            if application['name'] == name:
                userApplications.append(application)
                # db.delete(application['key'])
        return sorted(userApplications, key=lambda d: datetime.strptime(d['start'], '%Y-%m-%d').date())
    
    def deleteKeyApplication(self, key: str):
        #     """Delete leave application by key"""
        db = self.deta.Base("leaveApplications")
        allApplications = db.fetch().items
        for application in allApplications:
            if application['key'] == key:
                db.delete(application['key'])
        return
    
    def addUserApplication(self, name: str, start: datetime.date, end: datetime.date, type:str):
        #     """Add non-overlapping leave to the database"""
        db = self.deta.Base("leaveApplications")
        all_leaves = self.getUserApplication(name)
        success = True
        for leave in all_leaves:
            leave_start = datetime.strptime(leave['start'], '%Y-%m-%d').date()
            leave_end = datetime.strptime(leave['end'], '%Y-%m-%d').date()
            if (start < pd.Timestamp(leave_start)) and (end < pd.Timestamp(leave_start)):
                continue
            elif (start > pd.Timestamp(leave_end)) and (end > pd.Timestamp(leave_end)):
                continue
            else:
                message = 'Please delete overlapping leave before applying.'
                success = False
                return message, success
        db.put({"name": name, "start": str(start.date()), "end": str(end.date()), "type": type})
        message = "Leave applied successfully"
        return message, success
    

class publicHolidays:

    def __init__(self, local: bool):
        self.local = local
        if self.local:
           load_dotenv(".env")
           self.deta = Deta(os.getenv("DETA_KEY"))
        else:
           self.deta = Deta(st.secrets["DETA_KEY"])

    
    def getAllPublicHolidays(self):
        db = self.deta.Base("publicHolidays")
        return db.fetch().items[0]
    
    def getAllPublicHolidayName(self):
        allPublicHolidays = self.getAllPublicHolidays()
        ph = list(allPublicHolidays.keys())
        return ph
    
if __name__=="__main__":
    applications = leaveApplications(local=True)
    applications.addUserApplication(name="Elwin", start = datetime.now(), end = datetime.now(), type = 'Vacation Leave')