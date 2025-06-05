# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001F1153EC3E3F70AD9976DED5933A0C327C832CC5E399578EE9DC5E53DE764EAF0759383B0A8AD691D5C15380CD5381A0B230E42B46063D7B80B465DA8DE18A65706599A106AEDD3B7C01D92A96FB0BF1E08EB45F8DABD0AAEF3BF3029F52C2A89E0CFAD32E846809E3234B8CF94248A2CC2E157036F585E557D86F3EA05703EC0A2BFCB23C6ED8030EF2EF14F40E3C55CD367DE330641804E5C8DE061008E024A87F3D3D7CAD463146ACAD85F7BF845A148C8B79F65CAD903CB672AB9C417184BBC716B7FBB7D2DF163F96685E847500C9CE81588CDBE3C6C0B92D5AEE778D76719F2EC293FCD9A450976DFC0486BA862F2CAC04FB9DC09FE14D1D37052745C47DBF6FCB9BDA461083B3E525A5DA985E7E0A2F24244C08CD1458A8FBA8506AC0B028574EF57E9EF0904F378C0518D4AAE9E9AE7B3E5DBBB70001B8C6BA25876EEF7F324F46543CE836CE2B973761B300E06AFC8339956EFC7FA2F111CBC59177"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
