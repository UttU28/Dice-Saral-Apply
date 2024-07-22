import json
import os
import pypyodbc as odbc
from flask import Flask, render_template, request, redirect, url_for
from credential import *
from datetime import datetime, timezone

from applyJob import *

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
            SELECT allData.id, applyQueue.selectedResume, applyQueue.timeOfArrival 
            FROM applyQueue 
            JOIN allData ON applyQueue.id = allData.id 
            ORDER BY applyQueue.timeOfArrival ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        jobQueue = []
        for row in rows:
            data_dict = {'id': row[0],'selectedResume': row[1],'timeOfArrival': str(row[2])}
            jobQueue.append(data_dict)
        cursor.close()
        conn.close()
    return jobQueue

def removeFromQueue(jobID):
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()
    query = f"DELETE FROM applyQueue WHERE id = '{jobID}'"
    cursor.execute(query)
    conn.commit()
    print("Job Removed form Apply Queue")
    cursor.close()
    conn.close()

def updateTheJob(jobID, applyStatus):
    conn = odbc.connect(connectionString)
    cursor = conn.cursor()
    timestamp = int(datetime.now(timezone.utc).timestamp())
    query = f"""
        UPDATE allData
        SET myStatus = '{applyStatus}', decisionTime = {timestamp}
        WHERE id = '{jobID}';
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def fetchResumeList():
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



if __name__ == "__main__":
    try: loadChrome()
    except: pass
    jobQueue = fetchTheQueue()
    resumeData = fetchResumeList()
    for thisJob in jobQueue:
        jobID = thisJob['id']
        selectedResume = resumeData.get(thisJob['selectedResume'])
        applyStatus = applyDice(jobID, selectedResume)
        removeFromQueue(jobID)
        updateTheJob(jobID, applyStatus)
