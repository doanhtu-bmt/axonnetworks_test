# Data daily page - example: https://www.accuweather.com/en/vn/district-1/3554433/daily-weather-forecast/3554433
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
from utils import convertDowDate, convertSubDate, skip_ad, generate_xpath
from daily_details_data_page import DailyDetailsDataPage
import traceback
import time
import requests

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

    locators = {
        "grd_daily_datagrid" : ("xpath", '//div[contains(@class,"page-content")]'),
        "lbl_summary_datetime" : ("xpath", '//p[@class="module-title"]')
    }
            
    def get_daily_data(self):
        
        skip_ad(self.driver)

        # print(self.lbl_summary_datetime.text)
 
        daily_data = {}

        data_elements = self.grd_daily_datagrid.find_elements(By.XPATH, DailyDataPage.XPATH_GENERIC_DAILY_CARD)

        print("---------------------------------------------------------")
        for element in data_elements:
            # print(element.getAttribute("innerText"))

            parent_xpath = generate_xpath(element, "")

            details_link_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_DETAILS_LINK)
            details_link = details_link_element.get_attribute('href')
            print(details_link)

            dow_date_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_DOW_DATE)
            sub_date_element = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_SUB_DATE)
            date = convertDowDate(dow_date_element.text) + ", " + convertSubDate(sub_date_element.text)
            print(convertDowDate(dow_date_element.text) + ", " + convertSubDate(sub_date_element.text))

            high_temperature = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_TEMP_HIGH)
            temp = high_temperature.text

            print("Temperature: " + temp)

            main_weather = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_PHRASE)
            weather = main_weather.text
            print("Main Weather: " + weather)

            realfeel_text  = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_REALFEEL_TEXT)
            realfeel_value = element.find_element(By.XPATH, parent_xpath + DailyDataPage.XPATH_GENERIC_DAILY_CARD_REALFEEL_VALUE)
            real_feel = realfeel_text.text.replace("\n", " ")
            print(real_feel)

            daily_data[sub_date_element.text] = { 
                "details_link"  : details_link,
                "date"          : date,
                "temp"          : temp,
                "weather"       : weather,
                "real_feel"     : real_feel

            }

            #print(daily_data)

            print("---------------------------------------------------------")
        
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
                print(moment_link)
                moments_data[moment] = self.get_daily_details_data(moment_link)
            
            value["details"] = moments_data

            break


        return daily_data
    
    def __details_link_generator(self, details_link, moment):
        if "weather-today" in details_link:
            details_link = details_link.replace("weather-today", "daily-weather-forecast") + "?day=1"
        elif "weather-tomorrow" in details_link:
            details_link = details_link.replace("weather-tomorrow", "daily-weather-forecast") + "?day=2"
        
        
        details_link = details_link.replace("daily-weather-forecast", moment + "-weather-forecast")

        return details_link
    
    def get_daily_details_data(self, details_data_link, num_tries=3, wait_time=3):
        for i in range(num_tries):
            try:
                self.driver.get(details_data_link)
                daily_details_page = DailyDetailsDataPage(self.driver)
                return daily_details_page.get_daily_details_data()
            except:
                print("Error: " + traceback.format_exc())
                if i < num_tries - 1:
                    print("Retrying #{0}...".format(str(i)))
                    time.sleep(wait_time)
    
    def get_daily_details_data_by_http_request(self, details_data_link, num_tries=3, wait_time=3):
        resp = requests.get(details_data_link)
        html = resp.text

        print(html)



