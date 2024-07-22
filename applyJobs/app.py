import subprocess
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pypyodbc as odbc
from credential import *
from datetime import datetime, timezone
import schedule

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'

connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def applyTheJob():
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

    def clickTheDamnButton(imageName, sleepTime, max_search_time=10, search_interval=1):
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        region = (0, 0, screen_width, screen_height)
        
        while time.time() - start_time < max_search_time:
            location = pyautogui.locateOnScreen('images/'+imageName+'.png', region=region, confidence=0.8)  # Adjust confidence as needed
            if location is not None:
                center = pyautogui.center(location)
                pyautogui.moveTo(center)
                pyautogui.click()
                time.sleep(sleepTime)
                return True  # Return True when the button is clicked successfully
            else:
                print(f"Still haven't found {imageName}.png...")
                time.sleep(search_interval)

        print(f"{imageName}.png not found within the time limit.")
        return False  # Return False if the image was not found within the time limit

    def applyDice(jobID, selectedResume, thisDriver):
        print(jobID, selectedResume)
        if thisDriver is None: raise ValueError("Driver is not initialized. Call loadChrome() first.")
        
        thisDriver.get(f"https://www.dice.com/job-detail/{jobID}")
        time.sleep(7)
        try:
            clickTheDamnButton('apply',2)
            clickTheDamnButton('replaceResume',2)

            pyautogui.click()
            time.sleep(0.8)
            pyautogui.hotkey('ctrl','l')
            time.sleep(0.8)
            pyautogui.typewrite('C:/Users/iandm/Desktop/Dice-Saral-Apply/allResume')
            time.sleep(0.8)
            pyautogui.press('enter')
            time.sleep(0.8)
            for i in range(6):
                pyautogui.press('tab')
                time.sleep(0.2)
            time.sleep(0.5)
            pyautogui.typewrite(selectedResume)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)

            screen_width, screen_height = pyautogui.size()
            region = (screen_width // 2, 0, screen_width, screen_height)
            pyautogui.click(screen_width//2,screen_height//2)
            time.sleep(0.2)
            pyautogui.press(['tab']*3)
            pyautogui.press('enter')
            time.sleep(3.5)
            clickTheDamnButton('next',1)
            location = pyautogui.locateOnScreen('images/submit.png', region=region, confidence=0.8)
            pyautogui.moveTo(location)
            return 'applied'

        except Exception as e:
            print(f"Error clicking 'Easy apply' button: {e}")
            return 'error'
    
    chrome_driver_path = 'C:/chromeDriver/chromedriver.exe'  # Ensure the path is correct
    chromeApp = subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9002', '--user-data-dir=C:/chromeDriver/diceData/'])
    time.sleep(2)
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9002")
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    jobQueue = []
    resumeData = {}
    jobQueue = fetchTheQueue()
    resumeData = fetchResumeList()
    for thisJob in jobQueue:
        jobID = thisJob['id']
        selectedResume = resumeData.get(thisJob['selectedResume'])
        try: applyStatus = applyDice(jobID, selectedResume, driver)
        except: applyStatus = 'error'
        removeFromQueue(jobID)
        updateTheJob(jobID, applyStatus)
    chromeApp.terminate()


if __name__ == "__main__":
    applyTheJob()
    schedule.every(15).minutes.do(applyTheJob)

    while True:
        schedule.run_pending()
        sleep(1)
