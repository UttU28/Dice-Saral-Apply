import json
import os
import pypyodbc as odbc
from flask import Flask, render_template, request, redirect, url_for
from credential import *
from datetime import datetime, timezone

app = Flask(__name__)

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'

connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

jobQueue = []
resumeData = {}

def fetchTheQueue():
    global jobQueue
    if not jobQueue:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        query = """
            SELECT allData.id, allData.title, allData.description, allData.company, myQueue.timeOfArrival 
            FROM myQueue 
            JOIN allData ON myQueue.id = allData.id 
            ORDER BY myQueue.timeOfArrival ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        jobQueue = []
        for row in rows:
            data_dict = {'id': row[0],'title': row[1],'description': row[2],'company': row[3],'timeOfArrival': str(row[4])}
            jobQueue.append(data_dict)
        cursor.close()
        conn.close()
    return jobQueue

def removeFromQueue(jobID):
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()
    query = f"DELETE FROM myQueue WHERE id = '{jobID}'"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def addToApplyQueue(jobID, selectedResume):
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()
    timestamp = int(datetime.now(timezone.utc).timestamp())
    query = """
        INSERT INTO applyQueue (id, timeOfArrival, selectedResume)
        VALUES (?, ?, ?)
    """
    params = (jobID, timestamp, selectedResume)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def getResumeList():
    global resumeData
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()
    query = """SELECT * FROM resumeList"""
    cursor.execute(query)
    rows = cursor.fetchall()
    resumeData = {row[0]: row[1] for row in rows}
    cursor.close()
    conn.close()
    return resumeData


@app.route("/", methods=["GET", "POST"])
def home():
    global jobQueue
    global resumeData

    if request.method == "POST":
        jobID = request.form.get("job_id")
        action = request.form.get("action")
        
        if action == "apply":
            resumeID = request.form.get("resume_id")
            print(jobID, action, resumeID)
            addToApplyQueue(jobID, resumeID)
        elif action == "deny":
            print(jobID, action)
        removeFromQueue(jobID)

        jobQueue = [job for job in jobQueue if job['id'] != jobID]

    if not jobQueue: jobQueue = fetchTheQueue()
    if resumeData == {}: resumeData = getResumeList()
    if not jobQueue: return render_template("jobNotFound.html")

    return render_template("index.html", jobData=jobQueue[0], resumeData=resumeData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)
