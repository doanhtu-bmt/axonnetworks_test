import calendar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, datetime
import os

from selenium.webdriver.common.by import By

def generate_xpath(child_element, current):
    child_tag = child_element.tag_name
    if child_tag == "html":
        return "/html[1]" + current
    parent_element = child_element.find_element(By.XPATH, "..")
    children_elements = parent_element.find_elements(By.XPATH, "*")
    count = 0
    for i, children_element in enumerate(children_elements):
        children_element_tag = children_element.tag_name
        if child_tag == children_element_tag:
            count += 1
        if child_element == children_element:
            return generate_xpath(parent_element, "/" + child_tag + "[" + str(count) + "]" + current)
    return None

def skip_ad(driver):
    # ad_id = 'dismiss-button'
    # try:
    #     element = WebDriverWait(driver, 3).until(
    #     EC.presence_of_element_located((By.ID, ad_id)))
    #     #element = driver.find_element(By.XPATH, xpath)
    #     element.click()

    # except NoSuchElementException: 
    #     print("INFO: Ad not found, no need to skip ad") 
    

    # driver.click()
    ActionChains(driver).move_by_offset(50, 50).pause(2).click().perform()
    # ToDo: need to wait for data to load fully
    time.sleep(5)

def convertDowDate(dow_date):
    lower_dow_date = dow_date.lower()

    switcher = {
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday",
    }
 
    return switcher.get(lower_dow_date, "Error")

def convertSubDate(sub_date):
    date_ls = sub_date.split("/")
    month = int(date_ls[0])
    day   = date_ls[1]
    return calendar.month_name[month] + " " + day

def create_report_file(content):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join("reports", timestr + ".txt")
    f = open(path, "w")
    f.write(content)
    f.close()

def time_diff_for_displaying(first_time, later_time):
    difference = later_time - first_time
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    return divmod(difference.days * seconds_in_day + difference.seconds, 60)

