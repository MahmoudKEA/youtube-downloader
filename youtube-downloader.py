# Youtube-Downloader is a simple and easy tool to help students download their study materials from YouTube
# Powered by Engineer Mahmoud Khaled

import os
import json
import time

try:
    from pytube import YouTube
except ModuleNotFoundError:
    # // Library installation : pip install pytube
    os.system('pip3 install pytube')
    from pytube import YouTube


class YoutubeDownloader(object):
    def __init__(self):
        self.extension = None
        self.save_folder_dir = None
        self.videos_url_list = None

        self.__configure()

    def __configure(self):
        with open('config.json') as file:
            config = json.load(file)
        
        self.extension = config.get('extension')
        self.save_folder_dir = config.get('save_folder_dir')
        self.videos_url_list = config.get('videos_url_list')

    def __is_exists(self, filename: str, size: int):
        full_path = os.path.join(self.save_folder_dir, filename)
        if os.path.exists(full_path) and size == os.path.getsize(full_path):
            return True

        else:
            return False

    def __downloader(self, url: str):
        while True:
            try:
                video = YouTube(url)
                video = video.streams.filter(
                    progressive=True, file_extension=self.extension
                ).order_by('resolution').desc().first()

                print(" - Title :", video.title)

                if self.__is_exists(video.default_filename, video.filesize):
                    print("[ ! ] Canceled, Already Exists !")

                else:
                    print(" - Size : {:0.2f} MB".format(video.filesize / (1024 * 1024)))
                    print(" - Resolution :", video.resolution)
                    print("Downloading...")
                    video.download(self.save_folder_dir)
                    print("[ + ] Downloaded")

            except Exception as error:
                print("[ - ] Error Detected :", type(error), error)
                time.sleep(5)

            else:
                return

    def run(self):
        if not os.path.exists(self.save_folder_dir):
            os.makedirs(self.save_folder_dir)

        for index, url in enumerate(self.videos_url_list, start=1):
            print("%d - Starting for | %s" % (index, url))
            self.__downloader(url)
            print("\n\n")

        print("[ + ] Download Completed")


if __name__ == "__main__":
    main = YoutubeDownloader()
    main.run()
