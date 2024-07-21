import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json, os
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime, timezone

# Custom Library
from jobDescription import *
from dataHandling import *


chrome_driver_path = 'C:/chromeDriver'
# subprocess.Popen(['/usr/bin/google-chrome', '--remote-debugging-port=8989', '--user-data-dir=/home/midhdesk0/Desktop/GRE-Words/chromeData/'])
subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=8989', '--user-data-dir=C:/chromeDriver/diceData/'])
sleep(2)
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:8989")

# options.add_argument("--start-maximized")
options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)

driver.get("https://www.dice.com/jobs?q=python&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&language=en&jobSavedSearchId=a35866ec-a689-44de-8b57-29d44ca98f74")

# BASIC SETUP FOR FIRST TIME LOADING
def loadThePage(funDriver):
    selectElement = Select(WebDriverWait(funDriver, 10).until(EC.presence_of_element_located((By.ID, "pageSize_2"))))
    selectElement.select_by_value("100")
    sleep(5)
    totalPages = funDriver.find_element(By.CLASS_NAME, "pagination")
    totalPages = totalPages.find_elements(By.TAG_NAME, "li")
    totalPages = len(totalPages) - 2
    # todayButton = WebDriverWait(funDriver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='posted-date-option' and @data-cy-index='1']")))
    # todayButton.click()
    # sleep(2)
    contractsButton = funDriver.find_element(By.XPATH, "//li[@data-cy='facet-group-option' and @data-cy-value='CONTRACTS']").find_element(By.XPATH, ".//button")
    contractsButton.click()
    sleep(2)
    funDriver.execute_script("window.scrollTo(0, 0);")
    return totalPages

def writeTheJob(jobID, location, title, company):
    jsonFilePath = 'jobData.json'
    if os.path.exists(jsonFilePath):
        with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
            jobsData = json.load(jsonFile)
    else:
        jobsData = {}
    if jobID not in jobsData:
        jobsData[jobID] = int(datetime.now(timezone.utc).timestamp())
        description, datePosted, dateUpdated = getJobDescription(jobID)
        addNewJobSQL(jobID, location, title, company, description, datePosted, dateUpdated)
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
            json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    totalPages = loadThePage(driver)

    print("Done herer")
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    exampleElements = soup.select('div.card.search-card')
    for exampleElement in tqdm(exampleElements, desc="Processing Jobs"):
        if exampleElement.find('div', {'data-cy': 'card-easy-apply'}):
            jobID = exampleElement.select('a.card-title-link')[0].get('id').strip()
            location = exampleElement.select('span.search-result-location')[0].text.strip()
            title = exampleElement.select('a.card-title-link')[0].text.strip()
            company = exampleElement.select('[data-cy="search-result-company-name"]')[0].text.strip()
            writeTheJob(jobID, location, title, company)

    driver.quit()