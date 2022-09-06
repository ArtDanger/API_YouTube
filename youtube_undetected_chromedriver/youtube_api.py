import re

from selenium_driver import BaseClass

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import random


class YouTube(BaseClass):

    def __init__(self):
        super(YouTube, self).__init__()

        self.DRIVER = self.driver()

    def auth(self, login=str, password=str):

        """Authorization at the youtube"""

        self.DRIVER.get('http://youtube.com')

        time.sleep(random.uniform(7, 10))

        # Click button "Accept All" Agreed use all cookies
        if self.xpath_exists('//tp-yt-paper-dialog'):

            # check language == English(US)
            if not self.xpath_exists('//tp-yt-paper-button[@aria-label="English"]'):

                # click on the button with lang
                self.DRIVER.find_element(By.XPATH, value='//div[@class="style-scope ytd-consent-bump-v2-lightbox"]/ytd-button-renderer').click()

                # select English as main
                time.sleep(random.uniform(2, 3))
                self.DRIVER.implicitly_wait(10)
                self.DRIVER.find_element(By.XPATH, value='//option[./yt-formatted-string[text() = "English (US)"]]').click()

            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_element(By.XPATH,
                                     value='//tp-yt-paper-button[./yt-formatted-string[text() = "Accept all"]]').click()
            time.sleep(random.uniform(2, 3))

        # button войти
        if self.xpath_exists('//tp-yt-paper-button[@aria-label="Sign in"]'):
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-button[@aria-label="Sign in"]').click()

        # elif self.xpath_exists(''):
        #     pass
        # # enter login
        time.sleep(random.uniform(7, 10))
        self.DRIVER.implicitly_wait(10)
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(login)
        time.sleep(random.uniform(.5, 2))
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(Keys.ENTER)

        # enter password
        time.sleep(random.uniform(7, 10))
        self.DRIVER.implicitly_wait(10)
        self.DRIVER.find_element(By.XPATH, value='//input[@type="password"]').send_keys(password)
        time.sleep(random.uniform(.5, 2))
        self.DRIVER.find_element(By.XPATH, value='//input[@type="password"]').send_keys(Keys.ENTER)

        # press button "Not now" on question "If you’d like, take a few moments to help Google work better for you"
        # if self.xpath_exists('//button'):
        #     self.DRIVER.find_element(By.XPATH, value='//button').click()

        ### Here ADD NEW func on Auth

        # This func links on the self, if not icon account
        if self.xpath_exists('//tp-yt-paper-button[@aria-label="Sign in"]'):
            self.auth()

        return self.prepare_studio()

    def create_chanel(self):
        pass

    def prepare_studio(self):

        self.DRIVER.get("https://studio.youtube.com/channel/")
        time.sleep(random.uniform(7, 10))

        # creater chanek if new account
        if self.xpath_exists('//ytd-channel-creation-dialog-renderer'):
            # rename chanel xpath '//input[@aria-labelledby="paper-input-label-1"]'
            # button create chanel '//tp-yt-paper-button[@aria-label="СОЗДАТЬ КАНАЛ"]'
            # ToDo: app register account, change photo and rename on the chanel
            self.create_chanel()
            time.sleep(random.uniform(1, 2))

        # This table showing after creating new chanel(first enter)
        # if self.xpath_exists('//div[text()="Далее"]'):
        #     self.DRIVER.find_element(By.XPATH, value='//div[text()="Далее"]').click()
        #     time.sleep(random.uniform(3, 5))

    def founder_issues(self):

        # checker copyright(авторское право)
        self.DRIVER.implicitly_wait(5)
        copyright = self.DRIVER.find_element(By.XPATH, value='//div[@id="results-description"]').text
        if copyright == 'Checking if your video contains any copyrighted content':
            print(copyright)
            self.founder_issues()
        elif copyright == 'No issues found':
            print(copyright)

        elif re.findall(fr'(?im)\bThe owner allows\S*\b', copyright) == " The owner allows":
            print(copyright)

        else:
            print(type(copyright))
            print(copyright)
            raise Exception("video is blocked or prohibited by copyright")

    # press botton "Upload video"
    def page1_upload_video(self, path_to_video=str):

        # field for upload vidio on the youtube
        if self.xpath_exists('//input[@type="file"]'):
            print("Loadin video...")
            self.DRIVER.find_element(By.XPATH, value='//input[@type="file"]').send_keys(path_to_video)

    def page2_upload_video(self, title=str, tags=str):

        # title
        if self.xpath_exists('//div[@id="textbox"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[@id="textbox"]').clear()
            self.DRIVER.implicitly_wait(5)
            self.DRIVER.find_element(By.XPATH, value='//div[@id="textbox"]').send_keys(title)

            # check exists the radio-button "for kids"
            if self.xpath_exists('//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_MFK"]'):
                # click on the radio-button "for kids"
                self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button').click()

            # open new param, pressed button "Show more"
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Show more"]').click()

            # add tags
            time.sleep(random.uniform(5, 8))
            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_element(By.XPATH, value='//input[@aria-label="Tags"]').clear()
            self.DRIVER.find_element(By.XPATH, value='//input[@aria-label="Tags"]').send_keys('#shorts' + str(tags))

            # press button "Next"
            if self.xpath_exists('//div[text()="Next"]'):
                # from page "information" to "Adds"
                self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def page3_upload_video(self):
        # from page "Adds" to "Checker YouTube"
        time.sleep(random.uniform(2, 4))
        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def page4_upload_video(self):

        # check uploaded video on the copyright and banded content
        self.founder_issues()

        # from page "Checker YouTube" to access
        time.sleep(random.uniform(2, 4))
        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def page5_upload_video(self):
        # select radio-button public access
        time.sleep(random.uniform(1, 4))
        self.DRIVER.implicitly_wait(5)
        self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button[@name="PUBLIC"]/div').click()

        # while upload not completed
        def status():
            status_now = self.DRIVER.find_element(By.XPATH, value='//span[@class="progress-label style-scope ytcp-video-upload-progress"]').text
            print(status_now)
            if not status_now.split(".")[0] == "Checks complete":
                status()

        status()

        # press button upload
        time.sleep(random.uniform(1, 4))
        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-button[@id="done-button"]').click()

    def upload_video(self, path_to_file=str, title=str, tags=str):
        # press button "upload video" on the studia YouTube
        if self.xpath_exists('//ytcp-icon-button[@id="upload-icon"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-icon-button[@id="upload-icon"]').click()

        time.sleep(random.uniform(1, 3))

        # Check have limit today
        if self.xpath_exists('//div[text="Daily upload limit reached"]'):
            raise Exception("Daily upload limit reached")

        # pass page #1 for uploated video on the Youtube
        self.page1_upload_video(path_to_video=path_to_file)

        self.page2_upload_video(title=title, tags=tags)

        self.page3_upload_video()

        self.page4_upload_video()

        self.page5_upload_video()

        # finish work with Driver
        self.DRIVER.close()
        self.DRIVER.quit()
