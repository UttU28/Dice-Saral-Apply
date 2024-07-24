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

contentOut = ["security clearance", "security-clearance", "8+", "9+", "10+", "11+", "12+"]
contentIn = ["devops", "pipeline", "pipelines", "azure", "aws", "cloud", "cloud engineer", "cloud developer", "terraform", "ansible", "cicd", "ci-ci", "ci/cd", "kubernetes", "flask", "django", "FastAPI", "ETL"]


def scrapeTheJobs():
    def checkRequirementMatching(taroText, shouldBe, shouldNot):
        for temp1 in shouldBe:
            if temp1 in taroText:
                for temp2 in shouldNot:
                    if temp2 in taroText:
                        return False
                return True
        return False

    def writeTheJob(jobID, title, location, company):
        rawFilePath = 'rawData.json'
        rawData, jobsData = {},{}
        if os.path.exists(rawFilePath):
            with open(rawFilePath, 'r', encoding='utf-8') as jsonFile:
                rawData = json.load(jsonFile)
        else: rawData = {}

        jsonFilePath = 'jobData.json'
        if os.path.exists(jsonFilePath):
            with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
                jobsData = json.load(jsonFile)
        else: jobsData = {}

        if jobID not in rawData:
            jobsData[jobID] = int(datetime.now(timezone.utc).timestamp())
            description, datePosted, dateUpdated = getJobDescription(jobID)
            checkRequirements = checkRequirementMatching(description, contentIn, contentOut)
            if checkRequirements:
                addNewJobSQL(jobID, title, location, company, description, datePosted, dateUpdated)
                with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile: json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)
            with open(rawFilePath, 'w', encoding='utf-8') as jsonFile: json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)

    chrome_driver_path = 'C:/chromeDriver'

    options = Options()
    # options.headless = True
    # options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    options.add_argument("--disable-infobars")  
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    driver = webdriver.Chrome(options=options)

    jobKeyWords = ['DevOps', 'Azure devops', 'azure data']
    jobKeyWords = ['DevOps']
    exampleElements = []
    
    for jobKeyWord in jobKeyWords:
        print(jobKeyWord.replace(' ','%20'))
        driver.get(f"https://www.dice.com/jobs?q={jobKeyWord.replace(' ','%20')}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&filters.easyApply=true&language=en")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card.search-card')))
        except Exception as e:
            print(f"Exception occurred while waiting: {str(e)}")
        sleep(1)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')

        exampleElements.extend(soup.select('div.card.search-card'))

    driver.quit()

    for exampleElement in tqdm(exampleElements, desc="Processing Jobs"):
        if exampleElement.find('div', {'data-cy': 'card-easy-apply'}):
            jobID = exampleElement.select('a.card-title-link')[0].get('id').strip()
            location = exampleElement.select('span.search-result-location')[0].text.strip()
            title = exampleElement.select('a.card-title-link')[0].text.strip()
            company = exampleElement.select('[data-cy="search-result-company-name"]')[0].text.strip()
            writeTheJob(jobID, title, location, company)

if __name__ == "__main__":
    scrapeTheJobs()
    # schedule.every(15).minutes.do(scrapeTheJobs)

    # while True:
    #     schedule.run_pending()
    #     sleep(1)
