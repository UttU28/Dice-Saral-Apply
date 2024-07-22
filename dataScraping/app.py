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
from jobDescription import *
from dataHandling import *

def scrapeTheJobs():
    def loadThePage(funDriver):
        selectElement = Select(WebDriverWait(funDriver, 10).until(EC.presence_of_element_located((By.ID, "pageSize_2"))))
        selectElement.select_by_value("100")
        sleep(5)
        totalPages = funDriver.find_element(By.CLASS_NAME, "pagination")
        totalPages = totalPages.find_elements(By.TAG_NAME, "li")
        totalPages = len(totalPages) - 2
        todayButton = WebDriverWait(funDriver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='posted-date-option' and @data-cy-index='1']")))
        todayButton.click()
        sleep(2)
        contractsButton = funDriver.find_element(By.XPATH, "//li[@data-cy='facet-group-option' and @data-cy-value='CONTRACTS']").find_element(By.XPATH, ".//button")
        contractsButton.click()
        sleep(2)
        funDriver.execute_script("window.scrollTo(0, 0);")
        return totalPages

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

    chrome_driver_path = 'C:/chromeDriver'
    chromeApp = subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9001', '--user-data-dir=C:/chromeDriver/diceData/'])
    sleep(2)
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9001")
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.dice.com/jobs?q=python&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&language=en&jobSavedSearchId=a35866ec-a689-44de-8b57-29d44ca98f74")

    totalPages = loadThePage(driver)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')
    driver.quit()
    chromeApp.terminate()

    exampleElements = soup.select('div.card.search-card')
    for exampleElement in tqdm(exampleElements, desc="Processing Jobs"):
        if exampleElement.find('div', {'data-cy': 'card-easy-apply'}):
            jobID = exampleElement.select('a.card-title-link')[0].get('id').strip()
            location = exampleElement.select('span.search-result-location')[0].text.strip()
            title = exampleElement.select('a.card-title-link')[0].text.strip()
            company = exampleElement.select('[data-cy="search-result-company-name"]')[0].text.strip()
            writeTheJob(jobID, title, location, company)


if __name__ == "__main__":
    scrapeTheJobs()
    schedule.every(15).minutes.do(scrapeTheJobs)

    while True:
        schedule.run_pending()
        sleep(1)
