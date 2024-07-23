import pypyodbc as odbc
from flask import Flask, render_template, request, redirect, url_for
from credential import *
from datetime import datetime, timezone

app = Flask(__name__)

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'

# Define the connection pool - Ensure parameters are correctly specified
conn_pool = odbc.pooling.SimpleConnectionPool(
    1, 10, driver='{ODBC Driver 18 for SQL Server}',
    server='tcp:dice-sql.database.windows.net,1433',
    database='dice_sql_database',
    uid=username,
    pwd=password,
    encrypt='yes',
    trust_server_certificate='no',
    connection_timeout=30
)

def get_connection():
    return conn_pool.getconn()

def return_connection(conn):
    conn_pool.putconn(conn)

jobQueue = []
resumeData = {}

def fetchTheQueue():
    global jobQueue
    if not jobQueue:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT allData.id, allData.title, allData.description, allData.company, myQueue.timeOfArrival 
                FROM myQueue 
                JOIN allData ON myQueue.id = allData.id 
                ORDER BY myQueue.timeOfArrival ASC
            """
            cursor.execute(query)
            jobQueue = [
                {'id': row[0], 'title': row[1], 'description': row[2], 'company': row[3], 'timeOfArrival': str(row[4])}
                for row in cursor.fetchall()
            ]
    return jobQueue

def removeFromQueue(jobID):
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "DELETE FROM myQueue WHERE id = ?"
        cursor.execute(query, (jobID,))
        conn.commit()

def addToApplyQueue(jobID, selectedResume):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "INSERT INTO applyQueue (id, timeOfArrival, selectedResume) VALUES (?, ?, ?)"
        params = (jobID, timestamp, selectedResume)
        cursor.execute(query, params)
        conn.commit()

def getResumeList():
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM resumeList"
        cursor.execute(query)
        return {row[0]: row[1] for row in cursor.fetchall()}

@app.route("/", methods=["GET", "POST"])
def home():
    global jobQueue
    global resumeData

    if request.method == "POST":
        jobID = request.form.get("job_id")
        action = request.form.get("action")
        if action == "apply":
            resumeID = request.form.get("resume_id")
            addToApplyQueue(jobID, resumeID)
        elif action == "deny":
            pass
        removeFromQueue(jobID)
        jobQueue = [job for job in jobQueue if job['id'] != jobID]

    if not jobQueue:
        jobQueue = fetchTheQueue()
    if not resumeData:
        resumeData = getResumeList()
    if not jobQueue:
        return render_template("jobNotFound.html")

    return render_template("index.html", jobData=jobQueue[0], resumeData=resumeData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)

    # app.run()
