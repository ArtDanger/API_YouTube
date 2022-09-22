import time
import random

import pyperclip
import pyautogui

from .selenium_driver import BaseClass
from .exceptions import *

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException


class YouTube(BaseClass):

    def __init__(self):
        super(YouTube, self).__init__()
        self.DRIVER = None

    def __enter__(self):
        self.DRIVER = self.driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.close()
        self.DRIVER.quit()

    def __prepare_studio(self):

        self.DRIVER.get("https://studio.youtube.com/channel/")
        self.DRIVER.execute_script("window.onbeforeunload = function() {};")
        time.sleep(random.uniform(7, 10))

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

        if self.xpath_exists('//tp-yt-paper-button[./yt-formatted-string[text() = "Accept all"]]'):
            self.DRIVER.find_element(By.XPATH,
                                     value='//tp-yt-paper-button[./yt-formatted-string[text() = "Accept all"]]').click()
        elif self.xpath_exists(
                '//button[@aria-label="Accept the use of cookies and other data for the purposes described"]'):
            self.DRIVER.find_element(By.XPATH,
                                     value='//button[@aria-label="Accept the use of cookies and other data for the purposes described"]').click()
        else:
            # raise NotFoundException('Button "Accept all" not found.')
            input("Copy XPATH, send me and press ENTER")

        time.sleep(random.uniform(2, 3))

    def __enter_password(self, password):
        time.sleep(random.uniform(2, 3))

        # enter password
        if self.xpath_exists('//input[@type="password"]'):
            self.DRIVER.find_element(By.XPATH, value='//input[@type="password"]').send_keys(password)
            time.sleep(random.uniform(.5, 2))
            self.DRIVER.find_element(By.XPATH, value='//input[@type="password"]').send_keys(Keys.ENTER)

    def __backup_code(self, backup_codes=str):
        if self.xpath_exists('//button[./span[text()="Try another way"]]'):
            self.DRIVER.find_element(By.XPATH, '//button[./span[text()="Try another way"]]').click()

        if self.xpath_exists('//div[./div[text()="Enter one of your 8-digit backup codes"]]'):
            self.DRIVER.find_element(By.XPATH, '//div[./div[text()="Enter one of your 8-digit backup codes"]]').click()

            self.DRIVER.implicitly_wait(15)
            self.DRIVER.find_element(By.XPATH, '//input[@pattern="[0-9 ]*"]').send_keys(backup_codes)

            time.sleep(random.uniform(.8, 5))
            self.DRIVER.find_element(By.XPATH, value='//input[@pattern="[0-9 ]*"]').send_keys(Keys.ENTER)

        else:
            raise NotBackupCodeException("Backup option is not found.")

    def __auth(self, login=str, password=str, backup_code=None):

        # enter login
        self.DRIVER.implicitly_wait(10)
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(login)
        time.sleep(random.uniform(.5, 2))
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(Keys.ENTER)

        # enter password
        self.__enter_password(password)

        # func for authorization through backup code
        if self.xpath_exists('//button[./span[text()="Try another way"]]') or self.xpath_exists('//div[./div[text()="Enter one of your 8-digit backup codes"]]'):
            if backup_code is not None:

                self.__backup_code(backup_code)
                return True
            else:
                raise NotBackupCodeException("No backup codes.")
        else:
            raise NotBackupCodeException("Backup code not available. And google is not logged in")

        return False

    def auth_youtube(self, login=str, password=str, backup_codes=None):
        """
        Authorization at the youtube
        :return if False, this means function don't use your backup_code.
        :return if True. Function uses your backup_code.
        """

        self.DRIVER.get('http://youtube.com')

        time.sleep(random.uniform(7, 10))

        # Click button "Accept All" Agreed use all cookies
        if self.xpath_exists('//tp-yt-paper-dialog'):
            self.__cookie_agreement()

            # button Sign in
        if self.xpath_exists('//tp-yt-paper-button[@aria-label="Sign in"]'):
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-button[@aria-label="Sign in"]').click()

        elif self.xpath_exists('//ytd-button-renderer[@class="style-scope ytd-masthead"]'):
            self.DRIVER.find_elements(By.XPATH, value='//ytd-button-renderer[@class="style-scope ytd-masthead"]')[
                -1].click()

        else:
            self.DRIVER.get(
                "https://accounts.google.com/v3/signin/identifier?dsh=S-1844731254%3A1663145018237568&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Duk%26next%3D%252F&ec=65620&hl=uk&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AQDHYWqI46XR6XdqJ4nm8wk23jwJZQXfO8XxLsx77ETG0EfwFoRGFNhLmb2bfa7pBdyt4wgKphy7")

        use_backup_code = self.__auth(login, password, backup_codes)

        # This func links on the self, if not icon account
        if self.xpath_exists('//tp-yt-paper-button[@aria-label="Sign in"]'):
            self.__auth(login, password, backup_codes)

        return use_backup_code

    # def create_chanel(self):
    #     pass

    def __status(self):
        # check uploading video and access rights
        status_now = self.DRIVER.find_element(By.XPATH,
                                              value='//span[@class="progress-label style-scope ytcp-video-upload-progress"]').text

        if not status_now.split(".")[0] == "Checks complete":
            time.sleep(5)
            self.__status()

    def __founder_issues(self):

        # checker copyright(авторское право)

        copyright_elem = str(self.DRIVER.find_element(By.XPATH, value='//div[@id="results-description"]').text)
        if copyright_elem == 'Checking if your video contains any copyrighted content':
            print("... check copyright ...")
            time.sleep(10)
            self.__founder_issues()

        elif copyright_elem == 'No issues found':
            print(copyright_elem)

        elif copyright_elem.split('. ')[1] == 'People in some countries can’t watch your video.':
            print(copyright_elem)

        elif copyright_elem.split('. ')[1] == "The owner allows the content to be used on YouTube.":
            print(copyright_elem)

        else:
            input("New copytigt_elem, copy past and press enter: ")
            print(copyright_elem)
            raise VideoCopyrightException("When uploading to YouTube, the video was blocked due to copyright.")

    def __send_title(self, text=str):

        # fix Error ChromeDriver only supports characters in the BMP
        # now you can send emoji
        if self.xpath_exists('//div[@id="textbox"]'):
            # Ctrl + c
            pyperclip.copy(text)

            title_elem = self.DRIVER.find_element(By.XPATH, value='//div[@id="textbox"]')

            act = ActionChains(self.DRIVER)
            time.sleep(.5)
            act.move_to_element(title_elem)
            title_elem.clear()
            act.click(title_elem)

            # Ctrl + v
            act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL)
            act.perform()

            # if title not working, call error
            if self.xpath_exists(
                    '//ytcp-form-input-container[@class="invalid fill-height style-scope ytcp-social-suggestions-textbox style-scope ytcp-social-suggestions-textbox"]'):
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

            if self.xpath_exists(
                    '//ytcp-form-input-container[@class="style-scope ytcp-video-metadata-editor-advanced" and @invalid]'):
                raise FieldInvalidException("Field for tags is filled incorrectly. Most likely you have a long tag")

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

        # Check have limit today
        if self.xpath_exists('//div[text()="Daily upload limit reached"]'):
            raise LimitSpentException("Daily upload limit reached")

        self.__send_title(title)

        # check exists the radio-button "for kids"
        if self.xpath_exists('//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_MFK"]'):
            # click on the radio-button "for kids"
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button').click()

            # open new param, pressed button "Show more"
            if self.xpath_exists('//div[text()="Show more"]'):
                self.DRIVER.find_element(By.XPATH, value='//div[text()="Show more"]').click()
                time.sleep(random.uniform(.3, 1))

            else:
                raise NotFoundException('button "Show more" not found.')

            # add tags
            self.__send_tags(tags)

        else:
            raise NotFoundException('radio-button "VIDEO_MADE_FOR_KIDS_MFK" not found')

        self.__status()

        # select screensaver
        if self.xpath_exists('//ytcp-still-cell[@id="still-0"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-still-cell[@id="still-0"]').click()

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
            time.sleep(random.uniform(.3, 1))

        # press button upload
        if self.xpath_exists('//ytcp-button[@id="done-button"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-button[@id="done-button"]').click()

    def press_button_upload(self):
        
        # press button "upload video" on the studio YouTube
        if self.xpath_exists('//ytcp-icon-button[@id="upload-icon"]'):
            time.sleep(random.uniform(4, 8))
            self.DRIVER.find_element(By.XPATH, value='//ytcp-icon-button[@id="upload-icon"]').click()

        else:
            # raise NotFoundException('icon-button "upload-icon" not found.')
            input("copy XPATH and press Enter: ")

    def upload_video(self, path_to_file=str, title=str, tags=list):
        """Upload shorts video on the YouTube"""
        try:
            self.__prepare_studio()
            # press button "upload video" on the studio YouTube
            self.press_button_upload()

            time.sleep(random.uniform(.3, 1))

            # pass page #1 for uploaded video on the YouTube
            self._page1_upload_video(path_to_video=path_to_file)

            self._page2_upload_video(title=title, tags=tags)

            self._page3_upload_video()

            self._page4_upload_video()

            self._page5_upload_video()

            time.sleep(random.uniform(20, 40))

        except UnexpectedAlertPresentException:
            time.sleep(random.uniform(2, 5))
            pyautogui.press('tab')
            time.sleep(random.uniform(.5, 1.4))
            pyautogui.press('enter')

            time.sleep(random.uniform(20, 40))

    def get_backup_code(self, login, password, backup_code):
        """
        This function gets your google account 8-digit backup codes.

        :returns list backup codes
        """
        self.DRIVER.get('https://myaccount.google.com/u/1/security?hl=en')

        if self.xpath_exists('//a[text()="Sign in"]'):
            self.DRIVER.find_element(By.XPATH, '//a[text()="Sign in"]').click()

            # call authorization
            self.__auth(login, password, backup_code)

        if self.xpath_exists('//a[@aria-label="2-Step Verification"]'):
            self.DRIVER.find_element(By.XPATH, '//a[@aria-label="2-Step Verification"]').click()

            self.__enter_password(password)

            if self.xpath_exists('//div[./span[./span[text()="Get started"]]]'):
                # disabled 2-Step Verification -> Turn ON
                raise NotBackupCodeException("Disabled 2-Step Verification.")
                # self.DRIVER.find_element(By.XPATH, value='//div[./span[./span[text()="Get started"]]]').click()

            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_elements(By.XPATH, value='//a[@aria-label="Manage"]')[1].click()

            self.__enter_password(password)

            # refresh codes
            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_element(By.XPATH, '//button[@aria-label="Generate new codes"]').click()

            # window access
            self.DRIVER.implicitly_wait(10)
            self.DRIVER.find_element(By.XPATH, '//button[@data-mdc-dialog-action="ok"]').click()
            self.__enter_password(password)

            # get codes
            self.DRIVER.implicitly_wait(15)

            backup_codes = [str(el.text).replace(" ", "") for el in self.DRIVER.find_elements(By.XPATH, '//div[@dir]')]

            return backup_codes
