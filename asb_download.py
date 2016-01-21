from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import os
import time
from datetime import datetime


import secrets

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
download_dir = os.path.dirname(os.path.realpath(__file__))
profile.set_preference('browser.download.dir', download_dir)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/ofx')


driver = webdriver.Firefox(profile)
driver.get("https://online.asb.co.nz/auth/")

elem = driver.find_element_by_name("dUsername")
elem.send_keys(secrets.ASB_USERNAME)
elem = driver.find_element_by_name("password")
elem.send_keys(secrets.ASB_PASSWORD)
elem.send_keys(Keys.RETURN)


def DownloadStatement(startDate, endDate, accountName):

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, accountName)))
    element.click()

    elem = driver.find_element_by_id("Request_FromDate_inputDate")
    elem.clear()

    from_date = startDate.strftime('%d%m%Y')
    elem.send_keys(from_date)

    elem = driver.find_element_by_id("Request_ToDate_inputDate")
    elem.clear()
    to_date = endDate.strftime('%d%m%Y')
    elem.send_keys(to_date)

    elem = driver.find_element_by_id('exportEnabledDropdown')
    elem.click()

    elem = driver.find_element_by_id('ExportFormatDropdown_input_2')
    elem.click()

    time.sleep(3)

    driver.back()


# DownloadStatement(datetime(2016,1,1), datetime.today(), "Personal Account")
DownloadStatement(datetime(2016,1,1), datetime.today(), "Shared Account")


driver.close()