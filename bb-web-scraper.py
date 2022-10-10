import time
from utils.Sensor import Sensor
from utils.database import DatabaseCM
from utils.config import config
from multiprocessing import Process, Manager
from datetime import datetime


def check_load(db, sensors):
    last_load = time.time()
    while True:
        if datetime.now().strftime('%S') == '00':
            read_data(db, sensors)
        elif time.time() - last_load > 7200:
            print("Attempting restart due to timeout last load: "+str(time.time() - last_load))
            main()

def read_data(db, sensors):
    jobs = []
    soutput = Manager().list()
    for sensor in sensors:
        sensor_process = Process(target=sensor.get_data, args=(soutput, ))
        sensor_process.start()
        jobs.append(sensor_process)
    for job in jobs:
        job.join()
    load_data(db, soutput)
        
def load_data(db, sdata):
    load_count = 0
    for record in sdata:
        db.upload_sensor_data(record[0], record[1:])
        load_count += 1
    print("LOADED ITEMS: "+str(load_count))

def main():
    db = DatabaseCM()
    db.set_container(config["azure_storage"]["con_name"])

    sensors = []
    for stream in config["streams"]:
        sensors.append(Sensor(config["streams"][stream]["cam"], config["streams"][stream]["sensor_url"], config["streams"][stream]["timezone"]))
    
    loading_process = Process(target=check_load(db, sensors))
    loading_process.start()

if __name__ == '__main__':
    main()
