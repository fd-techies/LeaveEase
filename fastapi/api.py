from fastapi import FastAPI
from database import leaveApplications

app = FastAPI()
appliedLeaves = leaveApplications(local=True)

@app.get("/")
def getLeaveApplication(name: str):
    return appliedLeaves.getUserApplication(name)


#GET - Get an information
#POST - Create something new
#PUT - Update
#DELETE - Delete something