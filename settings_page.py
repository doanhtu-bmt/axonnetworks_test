from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support.ui import Select

class SettingsPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.accuweather.com/en/settings")

    locators = {
        "unit_selection"  : ("ID", "unit"),
    }

    def turn_settings_to_us_metrics(self):
        select = Select(self.unit_selection)

        # select by value 
        select.select_by_value("F")

    def turn_settings_to_iso_metrics(self):
        select = Select(self.unit_selection)

        # select by value 
        select.select_by_value("C")


