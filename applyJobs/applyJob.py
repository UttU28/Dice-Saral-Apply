import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

driver = None

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


def loadChrome():
    global driver
    chrome_driver_path = 'C:/chromeDriver/chromedriver.exe'  # Ensure the path is correct
    chromeApp = subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=9002', '--user-data-dir=C:/chromeDriver/diceData/'])
    time.sleep(2)
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9002")
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    return driver  # Return the driver instance

def applyDice(jobID, selectedResume):
    print(jobID, selectedResume)
    global driver
    if driver is None: raise ValueError("Driver is not initialized. Call loadChrome() first.")
    
    driver.get(f"https://www.dice.com/job-detail/{jobID}")
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
    

if __name__ == "__main__":
    loadChrome()  # Initialize the driver
    applyDice("cf9902a8-235b-4adb-a9d0-6f1c25688174")  # Use the driver to apply for a job
    applyDice("d6f03c2e-1197-4d79-bc91-0d83e08aa33b")  # Use the driver to apply for a job
