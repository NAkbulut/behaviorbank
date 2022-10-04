from utils.Sensor import Sensor
from utils.database import DatabaseCM
from utils.config import config
from multiprocessing import Process


def check_load(db, sensors):
    read_data(db, sensors)

def read_data(db, sensors):
    for sensor in sensors:
        sensor.set_driver()
        sdatetime, stemperature, shumidity, sprecipitation, swind = sensor.get_data()
        print(sdatetime, stemperature, shumidity, sprecipitation, swind)
        # sensor_process = Process(target=sensor.get_data)
        # sensor_process.start()

def main():
    # db = DatabaseCM()
    # db.set_container(config["azure_storage"]["con_name"])

    sensors = []
    for stream in config["streams"]:
        sensors.append(Sensor(config["streams"][stream]["cam"], config["streams"][stream]["sensor_url"], config["streams"][stream]["timezone"]))

    loading_process = Process(target=check_load(None, sensors))
    loading_process.start()

if __name__ == '__main__':
    main()
