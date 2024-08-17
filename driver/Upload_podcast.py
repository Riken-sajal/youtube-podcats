from driver.driver import Driver_class
from selenium.webdriver.common.by import By
from config import APPLE_USERNAME, APPLE_PASSWORD, SERVER_IP
import json, time
from app.models import  TwoFactorCode
from django.test import RequestFactory
from app.views import GenerateRSSFeed
from app.models import AudioFile


two_factor_code = None

class upload_podcast(Driver_class):
    def __init__(self):
        super().__init__(Apple_profile=True)

    def login_apple(self):
        global two_factor_code
        self.driver.get('https://appleid.apple.com/account/manage')
        sign_in_btn = self.find_element('Sign in Btn', "//button[contains(text(), 'Sign In')]", By.XPATH)
        if not sign_in_btn:
            self.driver.refresh()
            self.save_cookies()
            return True
        else:
            self.load_cookies()
            self.driver.refresh()

        sign_in_btn = self.find_element('Sign in Btn', "//button[contains(text(), 'Sign In')]", By.XPATH)
        if not sign_in_btn:
            self.save_cookies()
            return True

        self.driver.get('https://appleid.apple.com/sign-in')

        # switch to login iframe
        login_iframe = self.find_element('Login Iframe', 'aid-auth-widget-iFrame', By.ID)
        if login_iframe:
            self.driver.switch_to.frame(login_iframe)
            print("Switched to login frame")
        else:
            raise Exception("The login frame couldn't be found and can't further process")

        login_username_input = self.find_element('Login Email input', 'account_name_text_field', By.ID)
        if login_username_input:
            self.input_text(APPLE_USERNAME, 'Login Email input', 'account_name_text_field', By.ID)
            self.click_element('Sign in btn', 'sign-in', By.ID)

            Continue_with_password = self.find_element('Continue with password', 'continue-password', By.ID, timeout=2)
            if Continue_with_password:
                self.click_element('Continue with password', 'continue-password', By.ID)

            remember_me = self.find_element('remember me', 'remember-me', By.ID)
            if remember_me:
                if not remember_me.is_selected():
                    self.click_element('remember me', 'remember-me', By.ID)

            password_text_field = self.find_element('Login password input', 'password_text_field', By.ID)
            if password_text_field:
                self.input_text(APPLE_PASSWORD, 'Login Email input', 'password_text_field', By.ID)
                self.click_element('Sign in btn', 'sign-in', By.ID)

            if self.find_element('Two-factor auth input', 'form-security-code-inputs', By.CLASS_NAME):
                two_fact_inputs = self.driver.find_element(By.XPATH, '//div[@class="form-security-code-inputs"]')

                TwoFactorCode.objects.all().delete()
                print("Waiting for the two-factor authentication code...")
                while True:
                    two_factor_code = TwoFactorCode.objects.last()
                    if two_factor_code and two_factor_code.code:
                        two_factor_code = two_factor_code.code
                        break
                    time.sleep(1)

                if not two_factor_code.isdigit() or not len(two_factor_code) == 6:
                    raise Exception("Please Enter a valid 6-digit code")

                for auth_input, code in zip(two_fact_inputs.find_elements(By.TAG_NAME, 'input'), two_factor_code):
                    auth_input.send_keys(code)

                two_factor_code = None  # Reset the global variable for next use

            self.click_element('Trust_me', "//button[contains(text(), 'Trust')]", By.XPATH)
            self.save_cookies()

            return True
        self.save_cookies()
        self.Close_driver()


    def upload(self):


        self.driver.get('https://podcastsconnect.apple.com/')
        Podcast_title = self.find_element('Podcast_title', "//h1[contains(text(), 'Podcasts')]")
        if Podcast_title:
            self.click_element('+ Podcast btn', "//h1/div/button")
            self.click_element('add podcast New show', "//button[contains(text(), 'New Show')]")

            # self.click_element("add show with rss", "addFromFeed", By.ID)
            self.click_element("add show with rss", "createNew", By.ID)

            self.click_element('add podcast New show', "//button[contains(text(), 'Next')]")

            global  SERVER_IP
            if SERVER_IP.endswith('/') :
                SERVER_IP = SERVER_IP[:-1]

            if AudioFile.objects.all() :
                audio_object_latest = AudioFile.objects.all().latest('uploaded_at')
                self.input_text(f"{audio_object_latest.title}", "RSS feed url Input", '//input[@type="text"]')
            else :
                return False

            if self.find_element('add btn', "//button[contains(text(), 'Add')]") :
                self.random_sleep()
                if self.driver.find_elements(By.XPATH,"//button[contains(text(), 'Add')]"):
                    self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add')]")[-1].click()

            #     button[contains(text(), 'Add RSS Feed')]
            self.driver.switch_to.default_content()
            self.click_element('add podcast New show', '//*[@id="podcast-connect"]/div/div/div[2]/div[2]/div/div[2]/ul/li[1]/button')


            self.input_text(f"{SERVER_IP}/podcast/rss-feed/", "RSS feed url Input", '//textarea[@placeholder="https://podcast.example.com/feed.rss"]')
            if self.find_element('add podcast New show', "//button[contains(text(), 'Save')]"):
                self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Save')]")[-1].click()

            if self.find_element('add podcast New show', "//p[contains(text(), 'We’re still processing your show details. Check back later and then click Publish.')]") :
                self.random_sleep(10,15)
                
                self.driver.back()
                return True


        self.Close_driver()

    def publish(self):
        current_link = self.driver.current_url
        for i in self.driver.find_elements(By.XPATH,"//*[contains(@class,'show')]/div/a"):
            
            if self.find_element(By.XPATH,"//*[contains(text(), 'Publish')]") :
                
                self.random_sleep(10,15)
                self.click_element('copy rights third party','CLAIM_NO_THIRD_PARTY_CONTENT',By.ID)
                self.click_element('copy rights third party','//option[@value="RELEASE_OPTOUT"]',By.XPATH)
                self.click_element(By.XPATH,"//*[contains(text(), 'Save')]") 
                self.click_element(By.XPATH,"//*[contains(text(), 'Publish')]") 
            self.driver.back() if not self.driver.current_url  == current_link else None
