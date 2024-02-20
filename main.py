import logging
import webdrivers
from accuweather_mainpage import AccuWeatherMainpage
from settings_page import SettingsPage
from daily_data_page import DailyDataPage
from multiprocessing import freeze_support, set_start_method
from utils import time_diff_for_displaying, create_report_file

import time, datetime
import pprint

def test01():
  logging.info("Accuweather Test")

  freeze_support()
  set_start_method('spawn')

  start = datetime.datetime.now()

  driver = webdrivers.get_driver("firefox")

  page_settings = SettingsPage(driver)
  logging.info("Turn settings unit to Fahrenheit")
  page_settings.turn_settings_to_us_metrics()

  page_main = AccuWeatherMainpage(driver)
  page_main.navigate_to_daily_data_page()

  page_daily = DailyDataPage(driver)

  pp = pprint.PrettyPrinter(width=41, compact=True)

  current_location, summary_datetime, daily_data = page_daily.get_daily_data()
  pp.pprint(daily_data)
  driver.quit()

  # validation
  validation_result = True
  validation_failures = ""

  for date, data in daily_data.items():
    logging.info("Validating data for date {0}...".format(date))
    moments = ["morning", "afternoon", "evening", "overnight"]
    for moment in moments:
      logging.info("Validating data in the {0}...".format(moment))
      moment_data = data["details"][moment]
      temp_celcius = None
      if moment_data:
        temp_celcius = int(moment_data["temp_celcius"])
      
      temp_fahrenheit = None
      if moment_data:
        temp_fahrenheit = int(moment_data["temp_fahrenheit"])

      logging.info("Celcius temperature: " + str(temp_celcius))
      logging.info("Fahrenheit temperature: " + str(temp_fahrenheit))
      if temp_celcius and temp_fahrenheit:
        expected_fahrenheit = temp_celcius * 1.8 + 32
        expected_fahrenheit_rounded = round(expected_fahrenheit)
      else:
        logging.warning("Issue on getting temperature on {0}. Ignoring the validation".format(date))
        validation_failures += "Issue on getting temperature on {0}. Ignoring the validation".format(date) + "\n"
        validation_result = False
        continue

      logging.info("Expected Fahrenheit temperature: {0}".format(expected_fahrenheit))
      if expected_fahrenheit_rounded != temp_fahrenheit:
        logging.info("ERROR: Fahrenheit temperature and Celcius temperature is not matched on {0}".format(date))
        validation_failures += "ERROR: Temperatures in C & F are not matched on the {0} of {1}".format(moment, date) + ":\n"
        validation_failures += "       - Fahrenheit temperature is {0}, Celcius temperature is {1} - F (expected) = C({1}) * 1.8 + 32 = {2} (round to {3})"\
          .format(temp_fahrenheit, temp_celcius, expected_fahrenheit, expected_fahrenheit_rounded) + "\n"
        validation_result = False
      logging.info("Validating data in the {0}...Done".format(moment))
    logging.info("Validating data for date {0}...Done".format(date))

  end = datetime.datetime.now()
  (min, sec) = time_diff_for_displaying(start, end)
  logging.info("Time elapsed: {0} mins {1} seconds".format(min, sec))
  generate_report(current_location=current_location, summary_datetime=summary_datetime,
                  start_time=start, end_time=end, elapsed=(min, sec), validation_result=validation_result,
                  validation_failures=validation_failures, weather_data=daily_data)

def generate_report(current_location, summary_datetime, start_time, end_time, elapsed, validation_result,
                    validation_failures, weather_data):
  content =  "======Summary Report for querying and validating accuweather.com data======\n"
  content += "    - Current location: " + current_location + "\n"
  content += "    - Started on : " + start_time.strftime("%d/%m/%Y %H:%M:%S") + "\n"
  content += "    - Finished on: "   + end_time.strftime("%d/%m/%Y %H:%M:%S")   + "\n"
  content += "    - Queried data for {0} days. {1}".format(len(weather_data.keys()), summary_datetime) + "\n"
  content += "    - Time elapsed: {0} mins {1} seconds".format(*elapsed)   + "\n"
  if validation_result:
    content += "    - Validation result: PASSED" + "\n"
  else:
    validation_failures = validation_failures.splitlines()
    validation_failures = ["        - " + line + "\n" for line in validation_failures] 
    content += "    - Validation result: FAILED: \n" + "".join(validation_failures) + "\n"
  content += "===========================================================================\n"
  content += "  - Data :\n" + pprint.pformat(weather_data)
  create_report_file(content=content)

if __name__ == '__main__':
    #logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG)
    test01()