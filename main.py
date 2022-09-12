import os
import fnmatch
from Stream import Stream
from multiprocessing import Process
from pathlib import Path
from pytz import timezone
from datetime import datetime


streams = []
buff_th = 5
buff_dir = "staging_images"
tzmap = {"cam0" : "UTC"}

def check_images():
    while True:
        for cam_dir in Path().glob('cam*'):
            if len(fnmatch.filter(os.listdir(cam_dir), '*')) > buff_th:
                buffer_images(cam_dir)

def buffer_images(cam_dir):
    replace_count = 0
    for image in Path(str(cam_dir)).glob("*"):
        os.replace(str(cam_dir)+"/"+image.name, buff_dir+"/"+correct_timezone(image, tzmap.get(str(cam_dir))))
        replace_count += 1
    print("STAGED IMAGES: "+str(replace_count))

def load_images():
    # load images to database
    pass

def correct_timezone(image, tz):
    if tz == None: tz = 'Europe/Amsterdam'
    adj_tz = datetime.strptime((image.name.split('+')[1]), '%d-%m-%Y_%H-%M-%S.jpg').astimezone(timezone(tz))
    adj_tz = image.name.split('+')[0] + datetime.strftime(adj_tz, '+%d-%m-%Y_%H-%M-%S.jpg')
    return adj_tz

if __name__ == '__main__':

    streams.append(Stream("cam0", "https://www.youtube.com/watch?v=gcDWT-mTCOI", 10))
    streams.append(Stream("cam1", "https://www.youtube.com/watch?v=BQFGmIXwl-A", 10))

    for cam in streams:
        cam.simulate_url()
        cam_process = Process(target=cam.get_frames)
        cam_process.start()
    
    staging_process = Process(target=check_images)
    staging_process.start()
