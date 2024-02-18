# Data daily page - example: https://www.accuweather.com/en/vn/district-1/3554433/daily-weather-forecast/3554433
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
from utils import convertDowDate, convertSubDate, skip_ad, generate_xpath
from daily_details_data_page import DailyDetailsDataPage

from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait
from daily_details_data_page import DailyDetailsDataPage

import webdrivers
import traceback
import time
import threading
import logging
import psutil


class DailyDataPage(PageFactory):

    XPATH_GENERIC_DAILY_CARD = '//div[contains(@data-qa,"dailyCard")]'
    XPATH_GENERIC_DAILY_CARD_DETAILS_LINK =  '//a[@class="daily-forecast-card "]'
    XPATH_GENERIC_DAILY_CARD_DOW_DATE =  '//span[@class="module-header dow date"]'
    XPATH_GENERIC_DAILY_CARD_SUB_DATE =  '//span[@class="module-header sub date"]'
    XPATH_GENERIC_DAILY_CARD_TEMP_HIGH =  '//div[@class="temp"]/span[@class="high"]'
    XPATH_GENERIC_DAILY_CARD_PHRASE =  '//div[@class="phrase"]'
    XPATH_GENERIC_DAILY_CARD_REALFEEL_TEXT =  '//p[contains(text(), "RealFeel")]'
    XPATH_GENERIC_DAILY_CARD_REALFEEL_VALUE =  '//p[contains(text(), "RealFeel")]/span[@class="value"]'
    XPATH_GENERIC_DAILY_CARD_PRECIP =  '//div[@class="precip"]'

    def __init__(self, driver):
        self.driver = driver
        self.multi_process_readers = []

    locators = {
        "grd_daily_datagrid" : ("xpath", '//div[contains(@class,"page-content")]'),
        "lbl_summary_datetime" : ("xpath", '//p[@class="module-title"]')
    }
            
    def get_daily_data(self):
        
        skip_ad(self.driver)

        print("Collecting data in date range: ", self.lbl_summary_datetime.text)
 
        daily_data = {}
        data_elements = self.grd_daily_datagrid.find_elements(By.XPATH, DailyDataPage.XPATH_GENERIC_DAILY_CARD)

        logging.debug("---------------------------------------------------------")
        for element in data_elements:
            logging.debug(element.getAttribute("innerText"))

            parent_xpath = generate_xpath(element, "")

            details_link_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_DETAILS_LINK)
            details_link = details_link_element.get_attribute('href')
            logging.debug(details_link)

            dow_date_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_DOW_DATE)
            sub_date_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_SUB_DATE)
            date = convertDowDate(dow_date_element.text) + ", " + convertSubDate(sub_date_element.text)
            logging.debug(convertDowDate(dow_date_element.text) + ", " + convertSubDate(sub_date_element.text))

            high_temperature = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_TEMP_HIGH)
            temp = high_temperature.text

            logging.debug("Temperature: " + temp)

            main_weather = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_PHRASE)
            weather = main_weather.text
            logging.debug("Main Weather: " + weather)

            realfeel_text  = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_REALFEEL_TEXT)
            realfeel_value = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_REALFEEL_VALUE)
            real_feel = realfeel_text.text.replace("\n", " ")
            logging.debug(real_feel)

            daily_data[sub_date_element.text] = { 
                "details_link"  : details_link,
                "date"          : date,
                "temp"          : temp,
                "weather"       : weather,
                "real_feel"     : real_feel

            }
            #print(daily_data)
            logging.debug("---------------------------------------------------------")
        
        # get details data (humid, etc.)
        #return self.get_daily_details_data_sequencial(daily_data)
        return self.get_daily_details_data_parallel(daily_data)
    
    def get_daily_details_data_sequencial(self, daily_data):
        # get details data (humid, etc.)
        for key, value in daily_data.items():
            moments_data = {
                                "morning" : None,
                                "afternoon": None,
                                "evening": None,
                                "overnight": None
                            }
            for moment in moments_data.keys():
                moment_link = self.__details_link_generator(value["details_link"], moment)
                logging.debug(moment_link)
                moments_data[moment] = self.get_daily_details_data(moment_link)
            
            value["details"] = moments_data
        return daily_data
    
    def get_daily_details_data_parallel(self, daily_data, batches_run=15, limit_cpu_usage=100):
        # get details data (humid, etc.)
        self.multi_process_readers = []
        processes = []

        batches_process_running_control_thread = threading.Thread(target=self.__batches_process_running_control)
        is_thread_run = False

        for key, value in daily_data.items():

            moments_data = {
                                "morning" : None,
                                "afternoon": None,
                                "evening": None,
                                "overnight": None
                            }

            for moment in moments_data.keys():
                moment_link = self.__details_link_generator(value["details_link"], moment)
                logging.debug("Moment link: ", moment_link)
                cpu_percent = psutil.cpu_percent() 
                print(f"CPU utilization: {cpu_percent}%")
                while (len(self.multi_process_readers) > batches_run or cpu_percent > limit_cpu_usage):
                    if cpu_percent > limit_cpu_usage:
                        print(f"HIGH CPU utilization: {cpu_percent}% detected. On-hold starting new processes...")
                    time.sleep(0.5)
                    cpu_percent = psutil.cpu_percent()

                r, w = Pipe(duplex=False)
                self.multi_process_readers.append(r)
                process = Process(target=get_details_data_multiprocessing_supported, args=(w, moment_link))
                processes.append(process)
                process.start()
                w.close()

                if not is_thread_run:
                    batches_process_running_control_thread.start()
                    is_thread_run = True
        
        for process in processes:
            process.join()
        time.sleep(1)

        batches_process_running_control_thread.join()

        return daily_data
    
    def __batches_process_running_control(self):
        while self.multi_process_readers:
            for r in wait(self.multi_process_readers):
                try:
                    msg = r.recv()
                except EOFError:
                    self.multi_process_readers.remove(r)
                else:
                    logging.debug("Got message: ", msg)
                    #moments_data[moment] = self.get_daily_details_data(moment_link)
            
            #value["details"] = moments_data

    def __details_link_generator(self, details_link, moment):
        if "weather-today" in details_link:
            details_link = details_link.replace("weather-today", "daily-weather-forecast") + "?day=1"
        elif "weather-tomorrow" in details_link:
            details_link = details_link.replace("weather-tomorrow", "daily-weather-forecast") + "?day=2"
        
        details_link = details_link.replace("daily-weather-forecast", moment + "-weather-forecast")
        return details_link
    
    def get_daily_details_data(self, details_data_link, num_tries=3, wait_time=3, run_parallel=False):
        for i in range(num_tries):
            try:
                if run_parallel:
                    new_driver = webdrivers.get_driver("firefox")
                    daily_details_page = DailyDetailsDataPage(new_driver)
                else:
                    self.driver.get(details_data_link)
                    daily_details_page = DailyDetailsDataPage(self.driver)
                return daily_details_page.get_daily_details_data()
            except:
                logging.error("Error: " + traceback.format_exc())
                if i < num_tries - 1:
                    logging.error("Retrying #{0}...".format(str(i)))
                    time.sleep(wait_time)
    
def get_details_data_multiprocessing_supported(w, url):
    driver = webdrivers.get_firefox_driver()
    driver.get(url)
    page = DailyDetailsDataPage(driver)
    details_data = page.get_daily_details_data()
    driver.quit()

    details_data = {url : details_data}

    w.send(current_process().name + url + ": " + str(details_data))
    w.close()





