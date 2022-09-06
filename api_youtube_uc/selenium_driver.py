""" This file work with Selenium """

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class BaseClass:

    def __init__(self):  # add user-agent
        self.DRIVER = None


    def driver(self):

        chrome_options = uc.ChromeOptions()

        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-gpu")  # if headless

        # chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-extensions")  # отключает рассширения
        chrome_options.add_argument("--disable-popup-blocking")  # отключает блокировку всплывающих окон
        chrome_options.add_argument("--incognito")

        self.DRIVER = uc.Chrome(options=chrome_options)
        self.DRIVER.delete_all_cookies()
        self.DRIVER.maximize_window()

        return self.DRIVER


    def xpath_exists(self, xpath):

        try:
            self.DRIVER.implicitly_wait(15)
            self.DRIVER.find_element(By.XPATH, value=xpath)
            exist = True
        except NoSuchElementException:
            exist = False

        return exist