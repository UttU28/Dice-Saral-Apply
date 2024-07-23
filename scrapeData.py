import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json, os
from datetime import datetime, timezone
from tqdm import tqdm
import schedule

# Custom Library Imports - Ensure these paths are correct based on your project structure
from dataScraping.jobDescription import *
from dataScraping.dataHandling import *


def scrapeTheJobs():
    def writeTheJob(jobID, title, location, company):
        jsonFilePath = 'jobData.json'
        if os.path.exists(jsonFilePath):
            with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
                jobsData = json.load(jsonFile)
        else:
            jobsData = {}
        if jobID not in jobsData:
            jobsData[jobID] = int(datetime.now(timezone.utc).timestamp())
            description, datePosted, dateUpdated = getJobDescription(jobID)
            addNewJobSQL(jobID, title, location, company, description, datePosted, dateUpdated)
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
                json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)

    try:
        chrome_driver_path = 'C:/chromeDriver'
        # chromeApp = subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9001', '--user-data-dir=C:/chromeDriver/diceData/'])
        # sleep(2)
        # options = Options()
        # options.add_experimental_option("debuggerAddress", "localhost:9001")
        # options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
        # options.add_argument("--disable-notifications")
        # driver = webdriver.Chrome(options=options)

        options = Options()
        options.headless = True
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--disable-popup-blocking")  # Disable popup blocking
        options.add_argument("--disable-infobars")  
        options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
        driver = webdriver.Chrome(options=options)

        jobKeyWords = ['DevOps', 'Azure devops', 'azure data']

        for jobKeyWord in jobKeyWords:
            driver.get(f"https://www.dice.com/jobs?q={jobKeyWord.replace(' ','%20')}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&filters.easyApply=true&language=en")

            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, 'html.parser')

            exampleElements = soup.select('div.card.search-card')
            for exampleElement in tqdm(exampleElements, desc="Processing Jobs"):
                if exampleElement.find('div', {'data-cy': 'card-easy-apply'}):
                    jobID = exampleElement.select('a.card-title-link')[0].get('id').strip()
                    location = exampleElement.select('span.search-result-location')[0].text.strip()
                    title = exampleElement.select('a.card-title-link')[0].text.strip()
                    company = exampleElement.select('[data-cy="search-result-company-name"]')[0].text.strip()
                    writeTheJob(jobID, title, location, company)

        driver.quit()
        # chromeApp.terminate()
    except: print("\nSome error, look at next time")

if __name__ == "__main__":
    scrapeTheJobs()
    # schedule.every(15).minutes.do(scrapeTheJobs)

    # while True:
    #     schedule.run_pending()
    #     sleep(1)
