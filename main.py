import os
import fnmatch
from Stream import Stream
from Database import Database
from multiprocessing import Process
from pathlib import Path
from pytz import timezone
from datetime import datetime


streams = []
buff_th = 5
load_th = 10
buff_dir = "staging_images"
tzmap = {"cam0" : "UTC"}

def check_images():
    while True:
        for cam_dir in Path().glob('cam*'):
            if len(fnmatch.filter(os.listdir(cam_dir), '*')) > buff_th:
                buffer_images(cam_dir)

def check_load(db):
    while True:
        if len(fnmatch.filter(os.listdir(buff_dir), '*')) > load_th:
            load_images(db)


def buffer_images(cam_dir):
    replace_count = 0
    for image in Path(str(cam_dir)).glob("*"):
        os.replace(str(cam_dir)+"/"+image.name, buff_dir+"/"+correct_timezone(image, tzmap.get(str(cam_dir))))
        replace_count += 1
    print("STAGED IMAGES: "+str(replace_count))

def load_images(db):
    load_count = 0
    for image in Path(buff_dir).glob("*"):
        db.upload_blob(image.name, image), os.remove(image)
        load_count += 1
    print("LOADED IMAGES: "+str(load_count))

def correct_timezone(image, tz):
    if tz == None: tz = 'Europe/Amsterdam'
    adj_tz = datetime.strptime((image.name.split('+')[1]), '%d-%m-%Y_%H-%M-%S.jpg').astimezone(timezone(tz))
    adj_tz = image.name.split('+')[0] + datetime.strftime(adj_tz, '+%d-%m-%Y_%H-%M-%S.jpg')
    return adj_tz

if __name__ == '__main__':
    db = Database()
    db.set_container("frames")

    streams.append(Stream("cam0", "https://www.youtube.com/watch?v=gcDWT-mTCOI", 1))
    streams.append(Stream("cam1", "https://www.youtube.com/watch?v=6NIt6ibAD6I", 1))

    for cam in streams:
        cam.simulate_url()
        cam_process = Process(target=cam.get_frames)
        cam_process.start()
    
    staging_process = Process(target=check_images)
    staging_process.start()

    loading_process = Process(target=check_load(db))
    loading_process.start()
