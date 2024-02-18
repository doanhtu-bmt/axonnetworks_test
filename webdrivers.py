from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import traceback
import time


def get_driver(driver_name='firefox', num_tries=3):
    if driver_name == "firefox":
        return get_firefox_driver(num_tries)

def get_firefox_driver(num_tries=3):
    for i in range(num_tries):
        try:
            options = FirefoxOptions()
            options.headless = True
            return webdriver.Firefox(options=options)
        except:
            print("ERROR:" + traceback.format_exc())
            print("Wait 3s and retry")
            time.sleep(3)

def get_chrome_driver(num_tries=3):
    for i in range(num_tries):
        try:
            options = ChromeOptions()
            options.headless = True
            return webdriver.Chrome(options=options)
        except:
            print("ERROR:" + traceback.format_exc())
            print("Wait 3s and retry")
            time.sleep(3)