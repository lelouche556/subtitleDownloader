import time, re, os, click, requests
import hashlib
import glob
from bs4 import BeautifulSoup
import urllib.request

class Subtitle:
    #list of supported Languages
    Language_codes= {"Arabic": "ar","Chinese": "zh","English": "en"}
    # List of video file extensions this program supports
    VIDEO_EXTENSIONS = [
        ".avi", ".mp4", ".mkv", ".mpg",
        ".mpeg", ".mov", ".rm", ".vob",
        ".wmv", ".flv", ".3gp",".3g2"
    ]

    def __init__(self,file_path, language):
        self.file_path=path
        self.language=language
        
    #this hash function receives the name of the file and returns the hash code
    def get_hash(self):
        readsize = 64 * 1024
        with open(self.file_path, 'rb') as f:
            size = os.path.getsize(self.file_path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def get_subtitle(self):
        try:
            # skip if not a video file
            root, extension = os.path.splitext(self.file_path)
            if extension not in self.VIDEO_EXTENSIONS:
                print(self.file_path +"is not a video file ......Skipping")
                return
            
            Language_code=self.Language_codes[self.language]
            file_name= root + Language_code + ".srt"

            # if subtitle does not exist already
            if not os.path.exists(file_name):
                headers = { 'User-Agent' : 'SubDB/1.0 (Movie Subtitle Downloader/1.0; https://github.com/lelouche556/subtitleDownloader)' }
                url = "http://api.thesubdb.com/?action=download&hash=" + self.get_hash() + "&language=" + Language_code
                req = urllib.request.Request(url, None,headers)
                response = urllib.request.urlopen(req).read()

                with open(file_name, "wb") as subtitle: 
                    subtitle.write(response)
                    print(self.language + " subtitles successfully downloaded for " + self.file_path)
                    # logging.info(language + " subtitles successfully downloaded for " + file_path)
            
            else:
                print("Subtitle file is already downloaded")
        except:
            print(self.language + " subtitles not found for " + self.file_path + " in subdb")

path="/media/gaurav/Entertainment1/movies/hollywood/V.For.Vendetta.2006.720p.BrRip.x264.YIFY.mp4"
my_subtitle = Subtitle(path,"English")
my_subtitle.get_subtitle()

