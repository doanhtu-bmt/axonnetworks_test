from selenium import webdriver
import traceback
import time


def get_driver(driver_name='firefox', num_tries=3):
    if driver_name == "firefox":
        return get_firefox_driver(num_tries)

def get_firefox_driver(num_tries=3):
    for i in range(num_tries):
        try:
            return webdriver.Firefox()
        except:
            print("ERROR:" + traceback.format_exc)
            print("Wait 3s and retry")
            time.sleep(3)
