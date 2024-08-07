from driver.driver import Driver_class
from selenium.webdriver.common.by import By
from config import APPLE_USERNAME, APPLE_PASSWORD
import json


class upload_podcast(Driver_class):
    def __init__(self):
        super().__init__(Apple_profile=True)


    def login_apple(self):

        """
        This will help driver to login into the apple podcast and save the profile for later use
        :return:
        True if logged in successfully
        False if there is any issue in loggin
        """

        self.driver.get('https://appleid.apple.com/account/manage')
        sign_in_btn = self.find_element('Sign in Btn', "//button[contains(text(), 'Sign In')]", By.XPATH)
        if not sign_in_btn:
            self.driver.refresh()
            self.save_cookies()
            return True
        else :
            self.load_cookies()
            self.driver.refresh()


        sign_in_btn =  self.find_element('Sign in Btn', "//button[contains(text(), 'Sign In')]", By.XPATH)
        if not sign_in_btn :
            self.save_cookies()
            return True

        self.driver.get('https://appleid.apple.com/sign-in')


        # switch to login iframe
        login_iframe = self.find_element('Login Iframe','aid-auth-widget-iFrame',By.ID)
        if login_iframe :
            self.driver.switch_to.frame(login_iframe)
            print("Switched to login frame")
        else :
            raise "The login frame couldn't find and can't further process"


        login_username_input = self.find_element('Login Email input', 'account_name_text_field', By.ID)
        if login_username_input :
            self.input_text(APPLE_USERNAME,'Login Email input', 'account_name_text_field', By.ID)
            self.click_element('Sign in btn','sign-in',By.ID)

            Continue_with_password = self.find_element('Continue with password', 'continue-password', By.ID)
            if Continue_with_password:
                self.click_element('Continue with password', 'continue-password', By.ID)

            remember_me = self.find_element('remember me', 'remember-me', By.ID)
            if remember_me :
                if not remember_me.is_selected():
                    self.click_element('remember me', 'remember-me', By.ID)

            password_text_field = self.find_element('Login passowrd input', 'password_text_field', By.ID)
            if password_text_field:
                self.input_text(APPLE_PASSWORD, 'Login Email input', 'password_text_field', By.ID)
                self.click_element('Sign in btn','sign-in',By.ID)

            if self.find_element('Two-factor auth input','form-security-code-inputs',By.CLASS_NAME):
                two_fact_inputs = self.driver.find_element(By.XPATH,'//div[@class="form-security-code-inputs"]')
                auth_code = input('Press Enter the two factor auth :').strip()
                if not auth_code.isdigit():
                    raise "Please Enter only digits"

                elif not len(auth_code) == 6:
                    raise "Please Enter only 6 digits"

                for auth_input, code in zip(two_fact_inputs.find_elements(By.TAG_NAME, 'input'), auth_code):
                    auth_input.send_keys(code)


            self.click_element( 'Trust_me', "//button[contains(text(), 'Trust')]", By.XPATH)
            self.save_cookies()

            return True
        self.save_cookies()


    def upload(self, rss_feed : str = ''):
        if not rss_feed :
            print("Please Enter the rss feed to upload it")
            return False

        self.driver.get('https://podcastsconnect.apple.com/')

        Podcast_title = self.find_element('Podcast_title',"//h1[contains(text(), 'Podcasts')]")
        if Podcast_title :
            self.click_element('+ Podcast btn',"//h1/div/button")
            self.click_element('add podcast New show',"//button[contains(text(), 'New Show')]")

            self.click_element("add show with rss","addFromFeed", By.ID)
            self.click_element('add podcast New show',"//button[contains(text(), 'Next')]")
            self.input_text(rss_feed,"RSS feed url Input",'//textarea[@placeholder="https://podcast.example.com/feed.rss"]')
        #     http://52.78.1.26:8000
        #     New Show
