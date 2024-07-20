import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

driver = None

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

def applyDice(jobID):
    global driver

    if driver is None:
        raise ValueError("Driver is not initialized. Call loadChrome() first.")
    
    driver.get(f"https://www.dice.com/job-detail/{jobID}")
    
    
    # Use explicit wait to wait for the "Easy apply" button to be present
    try:
        screen_width, screen_height = pyautogui.size()
        region = (screen_width // 2, 0, screen_width // 2, screen_height)
        image_path = 'apply.png'  # Replace with the path to your image file
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)  # Adjust confidence as needed

        if location is not None:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y)
            pyautogui.click()
            print("Clicked on the image.")
        else:
            print("Image not found in the specified region.")
        easy_apply_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'apply-button.job-app'))
        )
        easy_apply_button.click()
        print("Clicked the 'Easy apply' button")
    except Exception as e:
        print(f"Error clicking 'Easy apply' button: {e}")
        return False
    
    # Wait for some time to ensure the page is fully loaded
    sleep(5)
    
    # Print the page source
    print(driver.page_source)

if __name__ == "__main__":
    loadChrome()  # Initialize the driver
    applyDice("cf9902a8-235b-4adb-a9d0-6f1c25688174")  # Use the driver to apply for a job
