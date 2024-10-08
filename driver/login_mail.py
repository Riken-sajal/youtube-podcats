from driver.driver import Driver_class
from selenium.webdriver.common.by import By
from config import GOOGLE_EMAIL, GOOGLE_PASSWORD
import subprocess, os, time
from fuzzywuzzy import process

two_factor_code = None

class Google(Driver_class):
    def __init__(self,google_profile=True):
        super().__init__(google_profile=google_profile)
        
    def login(self):
        login_url = 'https://www.google.com/intl/en-GB/gmail/about'
        self.driver.get(login_url)
        self.click_element("sign in btn",'/html/body/header/div/div/div/a[2]')
        self.input_text(GOOGLE_EMAIL,"Email input",'//*[@id="identifierId"]',By.XPATH)
        self.click_element("Next btn",'//*[@id="identifierNext"]/div/button')
        self.input_text(GOOGLE_PASSWORD,"Email input",'//*[@id="password"]/div[1]/div/div[1]/input',By.XPATH)
        self.click_element("Next btn",'//*[@id="passwordNext"]/div/button')
        self.click_element('Now now btn','//*[@id="yDmH0d"]/c-wiz[2]/div/div/div/div[2]/div[4]/div[1]/button',timeout=3)
        self.driver.get("https://www.youtube.com/")
        self.random_sleep()
        self.get_youtube()
        
    def get_youtube(self):
        self.driver.get("https://www.youtube.com/")
        
        
    def search_channel(self, channel_name):
        self.driver.get(f"https://www.youtube.com/@{channel_name}/videos")
        
    def load_videos(self,channel_name):
        def need_break(new_len_videos, old_len_videos):
            return new_len_videos == old_len_videos

        self.videos_link = []

        if not channel_name:
            raise "Please provide a valid Channel name"
        self.driver.get(f'https://www.youtube.com/@{channel_name}/videos')
        old_len_videos = 0

        while True:
            for _ in range(2):
                videos_grid = self.find_element('Videos grid',
                                                '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]')
                if not videos_grid: continue

                new_len_videos = len(self.driver.find_elements(By.XPATH,
                                                               '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/*'))
                try:
                    for _ in range(2):
                        try:
                            spinner_grid = self.find_element('Load video spinner',
                                                             '//tp-yt-paper-spinner[@id="spinner"]', timeout=2)

                            if spinner_grid:
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", spinner_grid)
                                self.random_sleep(2, 4)

                                break
                        except:
                            self.random_sleep(2, 4)
                except:
                    self.random_sleep(2, 4)

            print(new_len_videos, old_len_videos)
            if not need_break(new_len_videos, old_len_videos):
                old_len_videos = new_len_videos
                continue
            else:
                break
        
    def collect_videos(self, channel_name : str = ""):
        
        def modify_string(text):
            """keep only video url and their id"""
            parts = text.split('=')
            
            if len(parts) >= 3:
                first_part = parts[0] 
                second_part = parts[1].split()[0] 
                result = f"{first_part}={second_part}"
                return result
            return text 
        
        videos_link = []
        
        self.get_youtube()
        self.search_channel(channel_name)
        self.load_videos(channel_name)
        
        videos_grids = self.driver.find_elements(By.XPATH,
                                                 '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/*')
        for _ in range(3):
            try :
                for grid in videos_grids:
                    for video in grid.find_elements(By.XPATH, './/*[@id="content"]/*'):
                        video_link = video.find_element(By.XPATH, './/a[@id="video-title-link"]').get_attribute('href')
                        if not video_link in videos_link:
                            videos_link.append(modify_string(video_link))

                return videos_link
            except : ...

        return False 

               
    def download_videos(self,video_url):
        import difflib

        def string_similarity(file_name, title):
            # Calculate the similarity between the file name and the title
            return process.extractOne(title, [file_name])[1]

        def find_closest_match(title, directory):
            while True :
                # List all files in the directory
                files = os.listdir(directory)
                
                # Get the best match based on fuzzy matching
                matched_file, score = process.extractOne(title, files)
                
                if score > 75:  # You can adjust this threshold
                    return matched_file, score
                
                time.sleep(2)
        
        
            
            
        data = self.videos_data(video_url)
        self.driver.get("https://ytmp3s.nu/3vpx/")
        # https://www.youtube.com/watch?v=WXBnj1yRb5A
        self.input_text(video_url,"videos input for download",'//input[@id="url"]')
        self.find_element("videos input for download",'//input[@type="submit"]').submit()
        self.click_element("Download btn","/html/body/form/div[2]/a[1]", timeout=30)
        
        from utils.find_audio import find_from_downloads, find_from_ownpath
        
        while True :
            
            download_dir, file_path, found = find_from_downloads(data['title'])
            if found : break
            
            download_dir, file_path, found = find_from_ownpath(data['title'])
            if found : break
        
        # download_dir = f'/home/{get_local_username()}/Downloads'
        # # self.random_sleep(15,20)

        # while True:
        #     matched_file, similarity_score = find_closest_match(data['title'], download_dir)
        #     file_path = os.path.join(download_dir, matched_file)
            
        #     # Refresh the list of files in the directory to check the current state
        #     current_files = os.listdir(download_dir)
            
        #     # Check if the matching file (excluding .crdownload) is present in the directory
        #     if matched_file in current_files and ".crdownload" not in matched_file:
        #         print(f"Found and matched file: {file_path}")
        #         break
            
        #     # Check for the .crdownload version of the matched file
        #     crdownload_file = matched_file + ".crdownload"
        #     if crdownload_file in current_files:
        #         print("File is still downloading, waiting for completion...")
        #     else:
        #         print("File not found or download might have failed.")
            
        #     time.sleep(3)  # Wait for 3 seconds before checking again

        # for file in os.listdir(download_dir) :
        #     if data['title'] in file :
        #         file_path = os.path.join(download_dir, file)
        #         # while True :
        #         while True:
        #             if not ".crdownload" in file_path :
        #                 if string_similarity() > 75 :
                            
        #                 break
        #             elif not os.path.exists(file_path):
        #                 print(os.path.exists(file_path))
        #                 break
        #             else:
        #                 print("file could not found")
        #                 print(os.listdir(download_dir) )
        #                 time.sleep(3)
        #         print(file_path)
        #         break
        
        
    def calculate_duration(self,time_frame):
        
        pass
    
    def videos_data(self,video_url):
        tmp = {
            "file_path" : "",
            'length_in_seconds': "",
            'title': "",
            'description': "",
            'category' : ""
        }
        
        self.get_youtube()
        self.driver.get(video_url)
        
        title_ele = self.find_element("Title",'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]')
        if title_ele :
            tmp['title'] = title_ele.text
            
        self.click_element("More description",'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]')
        descripton_ele = self.find_element('Description','/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/yt-attributed-string')
        if descripton_ele :
            tmp['description'] = descripton_ele.text
            
        return tmp

