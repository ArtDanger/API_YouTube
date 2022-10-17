import time
import random

import pyautogui
import pyperclip
from selenium.webdriver import ActionChains

from .selenium_driver import BaseClass
from .exceptions import *

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException


class YouTube(BaseClass):
    """
    :profile = "Profile num" to be your Chrome "User Data"
    :browser_executable_path = (default path to Chrome) path to executable browser
    :user_data_dir = path copy your "User Data" with your only one profile (the most correct and safe way)
    """

    def __init__(self,
                 profile=str,
                 browser_executable_path=None,
                 user_data_dir=str):

        super(YouTube, self).__init__()
        self.profile = profile
        self.browser_executable_path = browser_executable_path
        self.user_data_dir = user_data_dir

    def __enter__(self):
        self.DRIVER = self._driver(profile=self.profile,
                                   user_data_dir=self.user_data_dir,
                                   browser_executable_path=self.browser_executable_path
                                   )
        self.act = ActionChains(self.DRIVER)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.close()
        self.DRIVER.quit()

    def __prepare_studio(self):
        links = [
            'https://mail.google.com',
            'https://news.google.com',
            'https://www.google.nl',
            'https://www.youtube.com',
            'https://www.google.nl',
            'https://translate.google.nl',
            'https://www.amazon.nl/',
        ]

        self.DRIVER.get(random.choice(links))
        time.sleep(random.uniform(2, 5))

        self.DRIVER.get(random.choice(links))
        time.sleep(random.uniform(2, 5))

        # attend YouTube Studio
        self.DRIVER.get("https://studio.youtube.com/channel/")

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

    def _auth(self, login=str, password=str, backup_code=None):

        # enter login
        self.DRIVER.implicitly_wait(10)
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(login)
        time.sleep(random.uniform(.5, 2))
        self.DRIVER.find_element(By.XPATH, value='//input[@type="email"]').send_keys(Keys.ENTER)

        # enter password
        self.__enter_password(password)

        # func for authorization through backup code
        if self.xpath_exists('//button[./span[text()="Try another way"]]') or self.xpath_exists(
                '//div[./div[text()="Enter one of your 8-digit backup codes"]]'):
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

        use_backup_code = self._auth(login, password, backup_codes)

        # This func links on the self, if not icon account
        if self.xpath_exists('//tp-yt-paper-button[@aria-label="Sign in"]'):
            self._auth(login, password, backup_codes)

        return use_backup_code

    def get_backup_code(self, login, password, backup_code):
        """
        This function gets your google account 8-digit backup codes.

        :returns list backup codes
        """
        self.DRIVER.get('https://myaccount.google.com/u/1/security?hl=en')

        if self.xpath_exists('//a[text()="Sign in"]'):
            self.DRIVER.find_element(By.XPATH, '//a[text()="Sign in"]').click()

            # call authorization
            self._auth(login, password, backup_code)

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

    # def create_chanel(self):
    #     pass

    def __status(self):
        # check uploading video and access rights

        status_now = self.DRIVER.find_element(By.XPATH,
                                              value='//span[@class="progress-label style-scope ytcp-video-upload-progress"]').text

        while not status_now.split(".")[0] == "Checks complete":

            time.sleep(random.uniform(2, 5))

            if self.xpath_exists('//div[text()="Processing abandoned"]', 3):
                text_error = self.DRIVER.find_element(By.XPATH,
                                                      value='//yt-formatted-string[@class="error-details style-scope ytcp-uploads-dialog"]').text
                raise PreventedThisUpload(text_error)

            status_now = self.DRIVER.find_element(By.XPATH,
                                                  value='//span[@class="progress-label style-scope ytcp-video-upload-progress"]').text

    def __send_text_JS(self, element, massage):
        self.DRIVER.execute_script(
            f'''
            const text = `{massage}`;
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text', text);
            const event = new ClipboardEvent('paste', {{
                clipboardData: dataTransfer,
                bubbles: true
            }});
            arguments[0].dispatchEvent(event)
            ''',
            element)

    def __send_title(self, text_title):

        if self.xpath_exists('//div[@id="textbox"]'):

            title_elem = WebDriverWait(self.DRIVER, 555).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="textbox"]')))
            self.DRIVER.execute_script("arguments[0].scrollIntoView(true);", title_elem)
            title_elem.click()
            title_elem.clear()
            time.sleep(random.uniform(.2, 1))

            # fix Error ChromeDriver only supports characters in the BMP
            # now you can send emoji
            self.__send_text_JS(massage=text_title, element=title_elem)

            # if title not working, call error
            if self.xpath_exists(
                    '//ytcp-form-input-container[@class="invalid fill-height style-scope ytcp-social-suggestions-textbox style-scope ytcp-social-suggestions-textbox"]',
                    3):
                raise FieldInvalidException("Title not filled in correctly.")

        else:
            raise NotFoundException("Title field not found.")

    def __send_tags(self, hashtags):
        # send tags on the textbox
        if self.xpath_exists('//input[@aria-label="Tags"]'):
            tags_elem = self.DRIVER.find_element(By.XPATH, value='//input[@aria-label="Tags"]')
            self.DRIVER.execute_script("arguments[0].scrollIntoView(true);", tags_elem)
            tags_elem.clear()
            self.act.move_to_element(tags_elem).click().perform()
            hashtags = ("shorts", *hashtags)

            for tag in hashtags:
                # self.__send_text_JS(massage=tag, element=tags_elem)
                pyperclip.copy(tag)
                self.act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
                tags_elem.send_keys(Keys.ENTER)

            if self.xpath_exists(
                    '//ytcp-form-input-container[@class="style-scope ytcp-video-metadata-editor-advanced" and @invalid]',
                    3):
                raise FieldInvalidException(
                    "Field for tags is filled incorrectly. Most likely you have a long tag.")
        else:
            NotFoundException("Tags field not found.")

    def __send_feedback(self):
        # send feedback
        if self.xpath_exists('//button[@key="cancel"]', 1):
            self.DRIVER.find_element(By.XPATH, '//button[@key="cancel"]').click()

    # press button "Upload video"
    def __page1_upload_video(self, *args):
        if len(args) > 1:
            paths = "\n".join(args)
        else:
            paths = str(args[0])

        # field for upload vidio on the youtube
        if self.xpath_exists('//input[@type="file"]'):
            self.DRIVER.find_element(By.XPATH, value='//input[@type="file"]').send_keys(paths)
            time.sleep(random.uniform(.5, 2))
        else:
            input("Copy xpath page 1: ")
            # raise NotFoundException("Video was not uploaded, XPATH may be missing.")

    def __page2_upload_video(self, title, tags):

        # check exists the radio-button "for kids"
        if self.xpath_exists('//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_MFK"]'):
            # click on the radio-button "for kids"
            WebDriverWait(self.DRIVER, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-radio-button'))).click()

            # open new param, pressed button "Show more"
            if self.xpath_exists('//div[text()="Show more"]'):
                self.DRIVER.find_element(By.XPATH, value='//div[text()="Show more"]').click()
                time.sleep(random.uniform(.1, 1))

            else:
                raise NotFoundException('button "Show more" not found.')

            # add title
            self.__send_title(title)

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
            self.__page2_upload_video(title, tags)

    def __page3_upload_video(self):
        # from page "Adds" to "Checker YouTube"
        time.sleep(random.uniform(.2, 1))
        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def __page4_upload_video(self):

        # from page "Checker YouTube" to access
        time.sleep(random.uniform(.2, 1))

        if self.xpath_exists('//div[text()="Next"]'):
            self.DRIVER.find_element(By.XPATH, value='//div[text()="Next"]').click()

    def __page5_upload_video(self):
        # select radio-button public access
        time.sleep(random.uniform(.2, 1))
        if self.xpath_exists('//tp-yt-paper-radio-button[@name="PUBLIC"]/div'):
            self.DRIVER.find_element(By.XPATH, value='//tp-yt-paper-radio-button[@name="PUBLIC"]/div').click()

            self.__send_feedback()

        # press button upload
        if self.xpath_exists('//ytcp-button[@id="done-button"]'):
            self.DRIVER.find_element(By.XPATH, value='//ytcp-button[@id="done-button"]').click()

            self.__send_feedback()

        time.sleep(random.uniform(3, 5))
        self.__close_popups()

    def __close_popups(self):
        # if new icon close (2way)
        if self.xpath_exists('//ytcp-button[@id="close-button"]/div', 555):
            self.click_element('//ytcp-button[@id="close-button"]/div')
        else:
            input("Copy Close: ")

    def __press_button_upload(self):

        # press button "upload video" on the studio YouTube
        if self.xpath_exists('//ytcp-icon-button[@id="upload-icon"]'):
            WebDriverWait(self.DRIVER, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//ytcp-icon-button[@id="upload-icon"]'))).click()

        elif self.xpath_exists('//ytcp-button[@id="create-icon"]'):
            WebDriverWait(self.DRIVER, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//ytcp-button[@id="create-icon"]'))).click()
            WebDriverWait(self.DRIVER, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-item[@test-id="upload-beta"]'))).click()

        else:
            input('New xpath. Copy xpath and send me.[upload button] :')

    def __filling_info(self, title, tags):
        try:
            self.__page2_upload_video(title=title, tags=tags)

            self.__page3_upload_video()

            self.__page4_upload_video()

            self.__page5_upload_video()

            self.__send_feedback()

        except UnexpectedAlertPresentException:
            print("Catch alert, please wait")

            try:
                WebDriverWait(self.DRIVER, 3).until(EC.alert_is_present())
                alert = Alert(self.DRIVER)
                time.sleep(random.uniform(4, 8))
                alert.accept()

            except TimeoutException:
                self.__send_feedback()

                # clear alert
                self.DRIVER.execute_script("window.onbeforeunload = function() {};")
                time.sleep(random.uniform(.2, 1))

                self.__send_feedback()

            self.__page5_upload_video()

    @staticmethod
    def _sort_info(*args):
        paths_to_video = ()
        titles = ()
        tags = ()

        for arg in args:
            path, title, *tag = arg
            paths_to_video = (*paths_to_video, path)
            titles = (*titles, title)
            tags = *tags, tag

        # return meta_videos
        return paths_to_video, titles, tags

    def upload_video(self, *args):
        """
        Upload shorts video on the YouTube
        example:
        path/to/video.mp4, "title", tags1, tags2, tags3, ... tagsN
        or
        (path_to_video, title, tags1, tags2, .... tagsN), (path_to_video, title, tags .... tagsN), ...
        Alert "Sorry, we were not able to save your video."

        """
        paths_video, titles, tags = YouTube._sort_info(*args)
        self.__prepare_studio()
        # press button "upload video" on the studio YouTube
        self.__press_button_upload()

        self.__page1_upload_video(*paths_video)

        # Check have limit today
        if self.xpath_exists(
                '//span[@id="progress-status-0" and contains(text(), "Daily upload limit reached")]',
                3) or self.xpath_exists('//div[text()="Daily upload limit reached"]', wait=3):
            raise LimitSpentException("Daily upload limit reached")

        # check if window exists
        if self.xpath_exists('//ytcp-multi-progress-monitor/tp-yt-paper-dialog', 10):
            # to get button to fill field
            # self.DRIVER.implicitly_wait(10)
            # elements_video = self.DRIVER.find_elements(By.XPATH, '//ul[@id="progress-list"]/li')

            for count, path_video in enumerate(paths_video):
                # if upload fail close browser
                if not self.xpath_exists(
                        f'//span[@id="progress-status-{count}" and contains(text(), "Daily upload limit reached")]', 3):
                    video_name = path_video.split("\\")[-1]

                    try:
                        WebDriverWait(self.DRIVER, 20).until(EC.element_to_be_clickable(
                            (By.XPATH, f'//button[@aria-label="Edit video {video_name}"]'))).click()

                        # execute filling form
                        try:
                            self.__filling_info(titles[count], tags[count])
                        except PreventedThisUpload:
                            self.DRIVER.find_element('//ytcp-icon-button[@aria-label="Save and close"]').click()
                            print(
                                f'YouTube prevented this upload because it’s a copy of a video "{video_name}" we removed in the past.')
                            continue

                    except UnexpectedAlertPresentException:
                        self.DRIVER.execute_script("window.onbeforeunload = function() {};")
                        self.__page5_upload_video()
                        continue
                else:
                    raise LimitSpentException("Daily upload limit reached")

            # Everything video uploaded and close browser
            while True:
                if self.xpath_exists('//span[text()="Uploads complete"]'):
                    break
                else:
                    time.sleep(random.uniform(5, 10))

        else:
            # unpicking tuple
            titles = titles[0]
            tags = tags[0]

            # upload 1 video
            try:
                self.__filling_info(titles, tags)

            except UnexpectedAlertPresentException:
                self.DRIVER.execute_script("window.onbeforeunload = function() {};")
                self.__page5_upload_video()
