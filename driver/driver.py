import random, time, os, random, re, json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from utils.extend_exp import expiry_extend

class Driver_class():


    def __init__(self,Apple_profile = False):
        # path for diffrent directories and other files
        self.download_path = os.path.join(os.getcwd(),'downloads')
        self.base_path = os.getcwd()
        self.cookies_file_path = os.path.join(self.base_path, 'cookies.json')

        # other variables to use later
        self.timeout = 10
        self.data = {}
        self.options = ''
        self.Apple_profile = Apple_profile

        # open the driver
        self.driver_args(Apple_profile)
        self.get_driver(Apple_profile)

        # diffrent variable to use late and need to open driver first to define it.
        self.wait_obj = WebDriverWait(self.driver, self.timeout)
        self.actions = ActionChains(self.driver)

    def driver_args(self, Apple_profile):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--lang=en')
        self.options.add_argument("--enable-webgl-draft-extensions")
        self.options.add_argument('--mute-audio')
        self.options.add_argument("--ignore-gpu-blocklist")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--enable-javascript")
        self.options.add_argument("--enable-popup-blocking")
        self.options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT {random.randint(6, 10)}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.{random.randint(3000, 4000)}.87 Safari/537.36")
        prefs = {
            "download.prompt_for_download": True,  # Always ask for download location
            "download.default_directory": "",  # Disable default directory for downloads
            "download_restrictions": 3,  # Block all downloads,
            'profile.default_content_setting_values.automatic_downloads': 1,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        self.options.add_experimental_option("prefs", prefs)

        if Apple_profile :

            # defining the profile directory path and if not exists directory then it will create
            profile_directory_path = os.path.join(self.base_path,'Apple_Profile')
            os.makedirs(profile_directory_path,exist_ok=True)

            # Add the profile arguments
            self.options.add_argument(
                f"--user-data-dir={profile_directory_path}")
            self.options.add_argument(r'--profile-directory=Profile 1')
        else :
            self.options.add_argument("--incognito")

        return  self.options

    def get_driver(self,Apple_profile):
        if not self.options in locals() :
            self.driver_args(Apple_profile)
        self.driver = webdriver.Chrome(options=self.options)


        self.driver.maximize_window()

    def save_cookies(self):
        """Save cookies to a file."""
        cookies = self.driver.get_cookies()

        for cookie in cookies :
            if "expiry" in cookie.keys() :
                cookie["expiry"] = expiry_extend(cookie["expiry"], 24)

        with open(self.cookies_file_path, 'w') as f:
            json.dump(cookies, f)
        print(f"Cookies saved to {self.cookies_file_path}")

    def load_cookies(self):
        """Load cookies from a file."""
        try :
            with open(self.cookies_file_path, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            print(f"Cookies loaded from {self.cookies_file_path}")
        except Exception as e:
            print(f"Error : {e} \nCookies could not load")
    def move_to_element(self, element):
        """this function will move to the element and make visible on the screen"""

        # redefining the actions variable to avoid errors
        if not self.actions:
            self.actions = ActionChains(self.driver)

        self.actions.move_to_element(element).perform()

    def random_sleep(self, a=5, b=8):
        """
        Random sleep time for few secounds
        Defualt secounds are 5 to 8 secounds
        """

        random_sleep_time = random.randint(a, b)
        print(f"random_sleep : {random_sleep_time}")
        time.sleep(random_sleep_time)

    def find_element(self, element, locator, locator_type=By.XPATH,
                     page=None, timeout=10,
                     condition_func=EC.presence_of_element_located,
                     condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(EC.presence_of_element_located((locator_type, locator)))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                                               value=locator)
            if page:
                print(
                    f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                      f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')

    def ensure_click(self, element: WebElement, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)

    def click_element(self, element, locator, locator_type=By.XPATH,
                      timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)

        if ele:
            self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();', ele)
            self.ensure_click(ele)
            print(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
                   timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""

        ele = self.find_element(element, locator, locator_type=locator_type,
                                timeout=timeout)

        if ele:
            for i in range(3):
                try:
                    ele.clear()
                    ele.send_keys(text)
                    print(f'Inputed "{text}" for the element: {element}')
                    return ele
                except ElementNotInteractableException:
                    print(" Error : ElementNotInteractableException")
                except Exception as e :
                    print(e)


    def ScrollDown(self, px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")
        
    def Close_driver(self):

        self.driver.quit()