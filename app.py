import json
from bs4 import BeautifulSoup
import os

with open('pageContent.html', 'r', encoding='utf-8') as file:
    htmlContent = file.read()

thisSoup = BeautifulSoup(htmlContent, 'html.parser')

jobID = thisSoup.select('a.card-title-link')[0].get('id').strip()
jobLocation = thisSoup.select('span.search-result-location')[0].text.strip()
jobTitle = thisSoup.select('a.card-title-link')[0].text.strip()
jobCompany = thisSoup.select('[data-cy="search-result-company-name"]')[0].text.strip()

job = {
    "title": jobTitle,
    "location": jobLocation,
    "company": jobCompany,
    "link": f"https://www.dice.com/job-detail/{jobID}",
    "isParsed": False,
}

jsonFilePath = 'jobData.json'
if os.path.exists(jsonFilePath):
    with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
        jobsData = json.load(jsonFile)
else:
    jobsData = {}

if jobID in jobsData:
    print("ID already exists. Skipping update.")
else:
    jobsData[jobID] = job
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
        json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)
