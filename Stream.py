import youtube_dl
import os


class Stream:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def simulate_url(self):
        ydl_opts = {
            'simulate': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url = self.url)
            self.simulation_url = video_info.get('url')

    def get_frames(self):
        ffmpeg_command = 'ffmpeg -i "'+self.simulation_url+'" -vf fps=10/60 '+self.name+'/image.cam0_%04d.jpg -loglevel quiet -hide_banner'
        os.system(ffmpeg_command)
