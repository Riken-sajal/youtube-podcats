import time
from app.models import AudioFile
from driver.driver import Driver_class
from selenium.webdriver.common.by import By


class Driver_bot(Driver_class):

    def load_all_videos(self, channel_name=""):
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

    def collect_videos_link(self, channel_name=""):
        self.load_all_videos(channel_name)
        videos_grids = self.driver.find_elements(By.XPATH,
                                                 '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/*')

        for _ in range(3):
            try :
                for grid in videos_grids:
                    for video in grid.find_elements(By.XPATH, './/*[@id="content"]/*'):
                        video_link = video.find_element(By.XPATH, './/a[@id="video-title-link"]').get_attribute('href')
                        if not video_link in self.videos_link:
                            self.videos_link.append(video_link)

                return self.videos_link
            except : ...

        return False
    
    def main(self, channel_name):
        vid_link_li = []
        for _ in range(3) :
            vid_link_li = self.collect_videos_link(channel_name)
            if not vid_link_li : continue
            return vid_link_li

        