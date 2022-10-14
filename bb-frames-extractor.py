import os
import fnmatch
import time
from utils.Stream import Stream
from utils.database import DatabaseCM
from utils.config import config
from multiprocessing import Process
from pathlib import Path
from pytz import timezone
from datetime import datetime


def check_images():
    while True:
        for cam_dir in Path().glob(config["directories"]["cams"]):
            if len(fnmatch.filter(os.listdir(cam_dir), '*')) > config["thresholds"]["buffer"]:
                buffer_images(cam_dir)

def check_load(db):
    last_load = time.time()
    while True:
        if len(fnmatch.filter(os.listdir(config["directories"]["buffer"]), '*')) > config["thresholds"]["load"]:
            load_images(db)
            last_load = time.time()
        elif time.time() - last_load > 7200:
            print("Attempting restart due to timeout last load: "+str(time.time() - last_load))
            main()

def buffer_images(cam_dir):
    replace_count = 0
    for image in Path(str(cam_dir)).glob("*"):
        try: 
            try: tz = config["streams"][str("stream" + (str(cam_dir).split("\\")[1])[-1])]["timezone"].replace('+', '%temp%').replace('-', '+').replace('%temp%', '-')
            except: tz = None
            os.replace(str(cam_dir)+"/"+image.name, config["directories"]["buffer"]+"/"+correct_timezone(image, tz))
        except:
            print("Moving to next fail due to stage image fail: "+image.name)
            continue
        replace_count += 1
    print("STAGED IMAGES: "+str(replace_count))

def load_images(db):
    load_count = 0
    for image in Path(config["directories"]["buffer"]).glob("*"):
        if db.upload_blob(image.name, image):
            load_count += 1
        os.remove(image)
    print("LOADED IMAGES: "+str(load_count))

def correct_timezone(image, tz):
    if tz == None: tz = 'Europe/Amsterdam'
    adj_tz = datetime.strptime((image.name.split('+')[1]), '%d-%m-%Y_%H-%M-%S.jpg').astimezone(timezone(tz))
    adj_tz = image.name.split('+')[0] + datetime.strftime(adj_tz, '+%d-%m-%Y_%H-%M-%S.jpg')
    return adj_tz

def main():
    db = DatabaseCM()
    db.set_container(config["azure_storage"]["con_name"])

    streams = []
    for stream in config["streams"]:
        streams.append(Stream(config["streams"][stream]["cam"], config["streams"][stream]["video_url"], config["streams"][stream]["fps"]))

    for cam in streams:
        cam.simulate_url()
        Path(config["directories"]["cams"].split('/')[0]+"/"+cam.name).mkdir(parents=True, exist_ok=True)
        cam_process = Process(target=cam.get_frames)
        cam_process.start()
    
    Path(config["directories"]["buffer"]).mkdir(parents=True, exist_ok=True)

    staging_process = Process(target=check_images)
    staging_process.start()

    loading_process = Process(target=check_load(db))
    loading_process.start()

if __name__ == '__main__':
    main()
