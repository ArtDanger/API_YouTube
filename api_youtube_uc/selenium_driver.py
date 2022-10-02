""" This file work with Selenium """
import glob
import os

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .exceptions import *


class BaseClass:

    def __init__(self):  # add user-agent
        self.DRIVER = None

    @staticmethod
    def find_profiles():
        """
        Finds all your profile in Chrome if you use Windows 10

        return: list exists Profiles
        """
        profiles = []
        absolute_path_profiles = glob.glob(
            os.environ['USERPROFILE'] + r"\AppData\Local\Google\Chrome\User Data\Profile" + '*')
        # return absolute_path_profiles
        for path_to_profile in absolute_path_profiles:  # get list profiles number
            profiles.append(path_to_profile.split("\\")[-1])

        if profiles:
            return profiles

        raise NotExistsProfileException("You don't have any profiles by path in Chrom on the Windows10")

    def _driver(self, profile, browser_executable_path):
        """
        Call driver via undetected_driver;

        if you pass profile:
            profile: your (Profile num)
        else:
            driver opens the incognito webpages and deletes cookies.
            Then you can use authorization on the YouTube

        return: driver
        """
        options = uc.ChromeOptions()

        if profile:

            # match on windows 10
            options.add_argument(fr"--user-data-dir={os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data")
            options.add_argument(f"--profile-directory={profile}")

            self.DRIVER = uc.Chrome(options,
                                    browser_executable_path=browser_executable_path,
                                    version_main=96,
                                    use_subprocess=True)
        else:

            options.add_argument("--incognito")

            self.DRIVER = uc.Chrome(options,
                                    browser_executable_path=browser_executable_path,
                                    version_main=96,
                                    use_subprocess=True)
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

    def click_element(self, xpath):

        if self.xpath_exists(xpath):
            self.DRIVER.find_element(By.XPATH, value=xpath).click()
        else:
            input("New xpath. Copy xpath and send me.")
