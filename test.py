import subprocess
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json, os
import pyperclip
from bs4 import BeautifulSoup


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

driver.get("https://www.dice.com/jobs?q=devops&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&language=en&jobSavedSearchId=a35866ec-a689-44de-8b57-29d44ca98f74")


def writeToFile(message):
    with open('pageContent.txt', 'w', encoding='utf-8') as file:
        file.write(str(message))

# BASIC SETUP FOR FIRST TIME LOADING
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

def writeTheJob(jobJson):
    jsonFilePath = 'jobData.json'
    if os.path.exists(jsonFilePath):
        with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
            jobsData = json.load(jsonFile)
    else:
        jobsData = {}

    if jobID in jobsData:
        print("ID already exists. Skipping update.")
    else:
        jobsData[jobID] = jobJson
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
            json.dump(jobsData, jsonFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    totalPages = loadThePage(driver)
    # BASIC SETUP FOR FIRST TIME LOADING

    print("Done herer")
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    exampleElements = soup.select('div.card.search-card')
    for exampleElement in exampleElements:
        
        jobID = exampleElement.select('a.card-title-link')[0].get('id').strip()
        jobLocation = exampleElement.select('span.search-result-location')[0].text.strip()
        jobTitle = exampleElement.select('a.card-title-link')[0].text.strip()
        jobCompany = exampleElement.select('[data-cy="search-result-company-name"]')[0].text.strip()

        job = {
            "title": jobTitle,
            "location": jobLocation,
            "company": jobCompany,
            "link": f"https://www.dice.com/job-detail/{jobID}",
            "isParsed": False,
        }

        writeTheJob(job)

    driver.quit()



    # sleep(2)
    # selectButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Select from computer']")))
    # selectButton.click()
    # # <button class=" _acan _acap _acas _aj1- _ap30" type="button"></button>
    # os.system("xdotool key ctrl+l")
    # sleep(1)

    # try:
    #     element = driver.find_element(By.CSS_SELECTOR, "._abfz._abg1")
    #     print("Element found.")
    #     element.click()
    # except NoSuchElementException:
    #     print("Element not found.")
    # # ratioButton.click()

    # captionText = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.xl565be.x5dp1im.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1w2wdq1.xen30ot.x1swvt13.x1pi30zi.xh8yej3.x5n08af.notranslate")))
    # captionText.click()
    # captionText.send_keys(removeBMP(thisCaption))

    # with open('uploadData.json', 'w') as file:
    #     json.dump(data, file, indent=4)
    # driver.quit()