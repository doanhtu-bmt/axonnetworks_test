from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
from utils import skip_ad

class DailyDetailsDataPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        skip_ad(self.driver)

    locators = {
        "lbl_humid" : ("xpath", '//p[contains(text(), "Humidity")]/span[@class="value"]')
    }
            
    def get_daily_details_data(self):
        #print("Humidity: " + self.lbl_humid.text)
        return { "humid" : self.lbl_humid.text }