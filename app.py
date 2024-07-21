import json, os
from flask import Flask, render_template, request, jsonify
from applyJob import *

app = Flask(__name__)

with open('jobData.json', 'r') as file:
    jobData = json.load(file)

directory = 'allResume'
allResumes = [filename for filename in os.listdir(directory) if filename.endswith('.pdf')]

jobList = list(jobData.items())
current_index = 0

def find_next_job():
    global current_index
    while current_index < len(jobList):
        jobID, jobDetails = jobList[current_index]
        if jobDetails.get("isApplied", "no") == "no":
            return jobID, jobDetails
        current_index += 1
    return None, None

@app.route("/", methods=["GET", "POST"])
def home():
    global current_index
    
    if request.method == "POST":
        action = request.form.get("action")
        selected_resume = request.form.get("resume")
        
        if action == "next":
            current_index += 1
            if current_index >= len(jobList):
                current_index = len(jobList) - 1
        
        elif action == "prev":
            current_index -= 1
            if current_index < 0:
                current_index = 0

        elif action in ["reject", "apply"]:
            jobID, jobDetails = jobList[current_index]
            if action == "apply":
                jobDetails["isApplied"] = applyDice(jobID, selected_resume)
            else:
                jobDetails["isApplied"] = False 
            jobData[jobID] = jobDetails

            jobID, jobDetails = find_next_job()
            if jobID and jobDetails:
                current_index = jobList.index((jobID, jobDetails))
            
            with open('jobData.json', 'w') as file:
                json.dump(jobData, file, indent=4)
        
        jobID, jobDetails = find_next_job()
        if jobID and jobDetails:
            return jsonify(jobDetails)
        else:
            return render_template("comeLater.html")
    
    jobID, jobDetails = find_next_job()
    if jobID and jobDetails:
        return render_template("index.html", jobDetails=jobDetails, allResumes=allResumes)
    else:
        return render_template("comeLater.html")

if __name__ == "__main__":
    try: loadChrome()
    except: pass
    app.run(host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5500)
