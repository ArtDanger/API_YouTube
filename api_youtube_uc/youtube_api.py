import re
import time
import random

import pyperclip

from .selenium_driver import BaseClass
from .exceptions import *

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class YouTube(BaseClass):

    def __init__(self):
        super(YouTube, self).__init__()
        self.DRIVER = None

    def __enter__(self):
        self.DRIVER = self.driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.DRIVER.quit()

    def __prepare_studio(self):

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

    def __cookie_agreement(self):

        """Agreement to use cookies."""
        # check language == English(US)
        if not self.xpath_exists('//tp-yt-paper-button[@aria-label="English"]'):
            # click on the button with lang
            self.DRIVER.find_element(By.XPATH,
                                     value='//div[@class="style-scope ytd-consent-bump-v2-lightbox"]/ytd-button-renderer').click()

            # select English as main
            time.sleep(random.uniform(2, 3))
            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_element(By.XPATH, value='//option[./yt-formatted-string[text() = "English (US)"]]').click()

        self.DRIVER.implicitly_wait(20)
        self.DRIVER.find_element(By.XPATH,
                                 value='//tp-yt-paper-button[./yt-formatted-string[text() = "Accept all"]]').click()
        time.sleep(random.uniform(2, 3))

    def auth(self, login=str, password=str):

        """Authorization at the youtube"""

        self.DRIVER.get('http://youtube.com')

        time.sleep(random.uniform(7, 10))

        # Click button "Accept All" Agreed use all cookies
        if self.xpath_exists('//tp-yt-paper-dialog'):
            self.__cookie_agreement()

        # button Sign in
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

            return self.__prepare_studio()

        else:
            raise NotFoundException('Button "Sign in" not found.')

    # def create_chanel(self):
    #     pass

    def __status(self):
        status_now = self.DRIVER.find_element(By.XPATH,
                                              value='//span[@class="progress-label style-scope ytcp-video-upload-progress"]').text
        print(status_now)

        if not status_now.split(".")[0] == "Checks complete":
            time.sleep(5)
            self.__status()

    def __founder_issues(self):

        # checker copyright(авторское право)

        copyright_elem = self.DRIVER.find_element(By.XPATH, value='//div[@id="results-description"]').text
        if copyright_elem == 'Checking if your video contains any copyrighted content':
            print(copyright_elem)
            time.sleep(5)
            self.__founder_issues()

        elif copyright_elem == 'No issues found':
            print(copyright_elem)

        elif re.findall(fr'(?im)\bThe owner allows\S*\b', copyright_elem)[0] == " The owner allows":
            print(copyright_elem)

        else:
            print(copyright_elem)
            raise VideoCopyrightException("When uploading to YouTube, the video was blocked due to copyright.")

        return self.__status()

    def __send_title(self, text=str):
        # fix Error ChromeDriver only supports characters in the BMP
        # now you can send emoji
        if self.xpath_exists('//div[@id="textbox"]'):
            # Ctrl + c
            pyperclip.copy(text)

            title_elem = self.DRIVER.find_element(By.XPATH, value='//div[@id="textbox"]')
            title_elem.clear()

            act = ActionChains(self.DRIVER)
            time.sleep(.5)
            self.DRIVER.implicitly_wait(5)
            act.move_to_element(title_elem)
            act.click(title_elem)

            # Ctrl + v
            act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL)
            act.perform()

            # if title not working, call error
            if self.xpath_exists('//ytcp-form-input-container[@class="invalid fill-height style-scope ytcp-social-suggestions-textbox style-scope ytcp-social-suggestions-textbox"]'):
                raise FieldInvalidException("Title not filled in correctly.")

        else:
            raise NotFoundException("Title field not found.")

    def __send_tags(self, hashtags=list):
        # send tags on the textbox
        if self.xpath_exists('//input[@aria-label="Tags"]'):
            tags_elem = self.DRIVER.find_element(By.XPATH, value='//input[@aria-label="Tags"]')
            tags_elem.clear()
            hashtags.insert(0, "#shorts")

            act = ActionChains(self.DRIVER)

            for tag in hashtags:
                # Copy
                pyperclip.copy(tag)
                act.click(tags_elem)

                # Past
                act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL)

                # performance of actions
                act.perform()
                if self.xpath_exists('//ytcp-form-input-container[@class="style-scope ytcp-video-metadata-editor-advanced" and @invalid]'):
                    raise FieldInvalidException("Field for tags is filled incorrectly.")

            else:
                NotFoundException("Tags field not found.")

    # press button "Upload video"
    def _page1_upload_video(self, path_to_video=str):

        # field for upload vidio on the youtube
        if self.xpath_exists('//input[@type="file"]'):
            self.DRIVER.find_element(By.XPATH, value='//input[@type="file"]').send_keys(path_to_video)
        else:
            raise NotFoundException("Video was not uploaded, XPATH may be missing.")

    def _page2_upload_video(self, title, tags):

        self.__send_title(title)

        # select screensaver
        if self.xpath_exists('//ytcp-still-cell[@id="still-0"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-still-cell[@id="still-0"]').click()

        # check exists the radio-button "for kids"
        if self.xpath_exists('//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_MFK"]'):
            # click on the radio-button "for kids"
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button').click()

            # open new param, pressed button "Show more"
            if self.xpath_exists('//div[text()="Show more"]'):
                self.DRIVER.find_element(By.XPATH, value='//div[text()="Show more"]').click()

            else:
                raise NotFoundException('button "Show more" not found.')

            # add tags
            self.__send_tags(tags)

        else:
            raise NotFoundException('radio-button "VIDEO_MADE_FOR_KIDS_MFK" not found')

        # press button "Next"
        if self.xpath_exists('//div[text()="Next"]'):
            # from page "information" to "Adds"
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

        else:
            self._page2_upload_video(title, tags)

    def _page3_upload_video(self):
        # from page "Adds" to "Checker YouTube"
        time.sleep(random.uniform(.3, 1))
        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def _page4_upload_video(self):

        # check uploaded video on the copyright and banded content
        self.__founder_issues()

        # from page "Checker YouTube" to access
        time.sleep(random.uniform(.3, 1))

        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

        else:
            self._page4_upload_video()

    def _page5_upload_video(self):
        # select radio-button public access
        time.sleep(random.uniform(.3, 1))
        if self.xpath_exists('//tp-yt-paper-radio-button[@name="PUBLIC"]/div'):
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button[@name="PUBLIC"]/div').click()

        else:
            raise NotFoundException('radio-button "PUBLIC" not found.')

        # press button upload
        time.sleep(random.uniform(.3, 1))
        # if self.xpath_exists('//ytcp-button[@id="done-button"]/div'):
        #     self.DRIVER.find_element(By.XPATH, value='//ytcp-button[@id="done-button"]/div').click()
        if self.xpath_exists('//div[text()="Publish"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Publish"]').click()

        else:
            raise NotFoundException('button "done-button" not found.')

    def upload_video(self, path_to_file=str, title=str, tags=list):
        # press button "upload video" on the studia YouTube
        if self.xpath_exists('//ytcp-icon-button[@id="upload-icon"]'):
            time.sleep(random.uniform(4, 8))
            self.DRIVER.find_element(By.XPATH, value='//ytcp-icon-button[@id="upload-icon"]').click()

        else:
            raise NotFoundException('icon-button "upload-icon" not found.')

        time.sleep(random.uniform(.3, 1))

        # Check have limit today
        if self.xpath_exists('//div[text="Daily upload limit reached"]'):
            raise LimitSpent("Daily upload limit reached")

        # pass page #1 for uploated video on the Youtube
        self._page1_upload_video(path_to_video=path_to_file)

        self._page2_upload_video(title=title, tags=tags)

        self._page3_upload_video()

        self._page4_upload_video()

        self._page5_upload_video()

    # def close_tab(self):
    #     self.DRIVER.close()


