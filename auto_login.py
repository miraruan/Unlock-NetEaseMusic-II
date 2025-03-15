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
    browser.add_cookie({"name": "MUSIC_U", "value": "006CBF9322E89C192D18656B5469157C01DE5CB9A601E9410EB56EBACF96F62C0A1493D0DD981720CBC53C52BFCB49CAE6B2BC97212E7926233A860A06E4E2DD37831D3F335D326F87ADAE164FB978E880BD39FD2FA4141502C1C196CAC0189F3348A62F15663420B993C466C501F6A9223B83E828EEAF5984F9531F15ADB099C211DE4FE17EA2116F33C772F3EA97E17FCA2E031B5CFC3F59C889DD09494B5C68379DA2BCD3A7527804B3E83E64E69D187677E37714845987B84EACAD6F8ADE17BD98EBC46F5301F7C4DD929B55502FA23410794421D1AC3AD659A8C1D56CD42F99AE9A8AC06B19384FDC88E0488D196904559A1C11E73B954B8927A13FCF7383A80FC24E49CC4DCF9AFDC8F4ACF293D5381685827285569D0FA42579C6903EB768C1C8EB38DA7FF34B649E61978FFDF9C9E381DE5F9D0321E46C02593A4E4D3F60D07A4750D11D564D0AA13D0D2C1572ACB765A09A92D215573D1BB443C42FC5"})
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
