import webdrivers
from accuweather_mainpage import AccuWeatherMainpage
from settings_page import SettingsPage
from daily_data_page import DailyDataPage
import pprint

from multiprocessing import freeze_support, set_start_method
import logging

import time

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG)

    freeze_support()
    set_start_method('spawn')

    start = time.time()

    driver = webdrivers.get_driver("firefox")

    page_settings = SettingsPage(driver)
    page_settings.turn_settings_to_us_metrics()

    page_main = AccuWeatherMainpage(driver)
    page_main.navigate_to_daily_data_page()

    page_daily = DailyDataPage(driver)

    pp = pprint.PrettyPrinter(width=41, compact=True)
    pp.pprint(page_daily.get_daily_data())
    driver.quit()

    end = time.time()
    print("Time elapsed: {0} seconds".format(end - start))
