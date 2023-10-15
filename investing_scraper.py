import asyncio
import functools
import time
import typing

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import re



def scrap():
    url = 'https://ca.investing.com/economic-calendar/'

    op = Options()

    op.add_argument("--no-sandbox")
    op.add_argument("--headless")
    op.add_argument("start-maximized")
    op.add_argument("window-size=1900,1080")
    op.add_argument("disable-gpu")
    op.add_argument("--disable-software-rasterizer")
    op.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=op)
    driver.get(url)

    driver.execute_script('scrollBy(0,300)')

    driver.find_element(By.XPATH, '//*[@id="timeFrame_tomorrow"]').click()
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="economicCurrentTime"]').click()
    driver.find_element(By.XPATH, '//*[@id="liTz5"]').click()
    time.sleep(10)
    driver.find_element(By.LINK_TEXT, 'Filters').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="calendarFilterBox_country"]/div[1]/a[2]').click()

    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="country6"]').click()
    driver.find_element(By.XPATH, '//*[@id="country72"]').click()
    driver.find_element(By.XPATH, '//*[@id="country22"]').click()
    driver.find_element(By.XPATH, '//*[@id="country35"]').click()
    driver.find_element(By.XPATH, '//*[@id="country12"]').click()
    driver.find_element(By.XPATH, '//*[@id="country5"]').click()
    time.sleep(2)
    driver.execute_script('scrollBy(0,-400)')
    driver.find_element(By.XPATH, '//*[@id="country25"]').click()
    driver.find_element(By.XPATH, '//*[@id="country37"]').click()
    driver.find_element(By.XPATH, '//*[@id="country17"]').click()
    driver.find_element(By.XPATH, '//*[@id="country4"]').click()
    driver.execute_script('scrollBy(0,400)')

    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="category_employment"]').click()
    driver.find_element(By.XPATH, '//*[@id="category_economicActivity"]').click()
    driver.find_element(By.XPATH, '//*[@id="category_centralBanks"]').click()
    driver.find_element(By.XPATH, '//*[@id="category_inflation"]').click()

    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="ecSubmitButton"]').click()
    time.sleep(3)
    driver.execute_script('scrollBy(0,-1000)')
    time.sleep(10)

    data_table = driver.find_element(By.XPATH, '//*[@id="economicCalendarData"]/tbody')

    value_list = []

    for row in data_table.find_elements(By.TAG_NAME, "tr"):
        t = []
        for cl in row.find_elements(By.TAG_NAME, "td"):
            if cl.text and cl.text!=' ':
                t.append(cl.text)
        if t:
            value_list.append(t)

    print(value_list)

    result_list = []

    for i in range(1, len(value_list)):
        result_list.append([value_list[i][2], value_list[i][0], value_list[i][1]])

    driver.quit()
    print(result_list)
    return result_list




