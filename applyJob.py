import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

driver = None

def clickTheDamnButton(konsa, kitnaSona):
    screen_width, screen_height = pyautogui.size()
    region = (screen_width // 2, 0, screen_width, screen_height)
    location = pyautogui.locateOnScreen('images/'+konsa+'.png', region=region, confidence=0.8)  # Adjust confidence as needed
    if location is not None:
        center = pyautogui.center(location)
        pyautogui.moveTo(center.x, center.y)
        pyautogui.click()
        sleep(kitnaSona)

def loadChrome():
    global driver
    chrome_driver_path = 'C:/chromeDriver/chromedriver.exe'  # Ensure the path is correct
    
    subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', 
                      '--remote-debugging-port=8989', 
                      '--user-data-dir=C:/chromeDriver/diceData/'])
    sleep(2)
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:8989")
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    options.add_argument("--disable-notifications")
    
    driver = webdriver.Chrome(options=options)
    
    return driver  # Return the driver instance

def applyDice(jobID, selectedResume):
    global driver
    if driver is None: raise ValueError("Driver is not initialized. Call loadChrome() first.")
    
    driver.get(f"https://www.dice.com/job-detail/{jobID}")
    sleep(7)
    try:
        clickTheDamnButton('apply',3)
        clickTheDamnButton('replaceResume',2)

        pyautogui.click()
        sleep(0.8)
        pyautogui.hotkey('ctrl','l')
        sleep(0.8)
        pyautogui.typewrite('C:/Users/iandm/Desktop/Dice-Saral-Apply/allResume')
        sleep(0.8)
        pyautogui.press('enter')
        sleep(0.8)
        for i in range(6):
            pyautogui.press('tab')
            sleep(0.2)
        sleep(0.5)
        pyautogui.typewrite(selectedResume)
        sleep(0.5)
        pyautogui.press('enter')
        sleep(1)

        # clickTheDamnButton('upload',5)
        # clickTheDamnButton('next',5)
        screen_width, screen_height = pyautogui.size()
        region = (screen_width // 2, 0, screen_width, screen_height)
        pyautogui.click(screen_width//2,screen_height//2)
        sleep(0.2)
        pyautogui.press(['tab']*3)
        pyautogui.press('enter')
        sleep(3.5)
        clickTheDamnButton('next',1)
        location = pyautogui.locateOnScreen('images/submit.png', region=region, confidence=0.8)
        pyautogui.moveTo(location)

        print("Clicked the 'Easy apply' button")
    except Exception as e:
        print(f"Error clicking 'Easy apply' button: {e}")
        return False
    

if __name__ == "__main__":
    loadChrome()  # Initialize the driver
    applyDice("cf9902a8-235b-4adb-a9d0-6f1c25688174")  # Use the driver to apply for a job
    applyDice("d6f03c2e-1197-4d79-bc91-0d83e08aa33b")  # Use the driver to apply for a job
