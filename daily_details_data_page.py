from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
from utils import skip_ad

class DailyDetailsDataPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        skip_ad(self.driver)

    locators = {
        "lbl_humid"         : ("xpath", '//p[contains(text(), "Humidity")]/span[@class="value"]'),
        "lbl_temperature"   : ("xpath", '//div[@class="weather"]//div[@class="temperature"]'),
        "lbl_temp_unit"     : ("xpath", '//span[@class="header-temp"]//span[@class="unit"]')
    }

    def get_current_temp_unit(self):
        if self.lbl_temp_unit.text.lower() == "f":
            return "fahrenheit"
        else:
            return "celcius"
          
    def get_daily_details_data(self):
        #print("Humidity: " + self.lbl_humid.text)
        #print("Temerature: " + self.lbl_temperature.text.replace("\u00b0", ""))
        return { "humid" : self.lbl_humid.text, ("temp_" + self.get_current_temp_unit()) : self.lbl_temperature.text.replace("\u00b0", "") }