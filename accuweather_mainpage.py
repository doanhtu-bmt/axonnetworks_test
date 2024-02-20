from seleniumpagefactory.Pagefactory import PageFactory
import logging

class AccuWeatherMainpage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.accuweather.com")

    locators = {
        "btn_hamburger"  : ("xpath", '//div[@class="pull-right"]/*[@data-qa="navigationMenu"]'),
        "mnu_data_daily" : ("xpath", '//a[@data-page-id="daily"]'),
    }

    def navigate_to_daily_data_page(self):
        logging.info("Navigating to daily data page...")
        self.btn_hamburger.click()
        self.mnu_data_daily.click()
        logging.info(self.driver.title)
        logging.info("Navigating to daily data page...Done")
        