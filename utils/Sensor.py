from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pytz import timezone
from datetime import date, datetime


class Sensor:
    def __init__(self, name, url):
        self.name = name
        self.url = url

        options = Options()
        options.add_argument("--headless")
        options.add_argument("log-level=1")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(10)

    def get_data(self):
        self.driver.get(self.url)
        thermal = self.driver.find_element(By.XPATH, '//div[@class="col-6 pb-20"]')
        conditions = self.driver.find_element(By.XPATH, '//div[@class="col-6 pb-20 pl-50"]')
        sdatetime, stemperature, shumidity, sprecipitation, swind = self.parse_data(conditions, thermal)
        print(f"Datetime: {sdatetime}\nTemperature: {stemperature}\nHumidity: {shumidity}\nPrecipitation: {sprecipitation}\nWind: {swind}")
    
    def parse_data(self, conditions, thermal):
        stemperature = int(thermal.find_elements(By.TAG_NAME, 'li')[1].get_attribute('textContent').split("°")[0])
        sdatetime = float(thermal.find_elements(By.TAG_NAME, 'li')[0].get_attribute('innerHTML').split("\"")[1])
        stimezone = str(thermal.find_elements(By.TAG_NAME, 'li')[0].get_attribute('innerText').split(" ")[1])
        shumidity = int(conditions.find_elements(By.TAG_NAME, 'li')[0].get_attribute('textContent').split(" ")[1][0:-1])
        sprecipitation = int(conditions.find_elements(By.TAG_NAME, 'li')[1].get_attribute('textContent').split(" ")[1][0:-1])
        swind = float(conditions.find_elements(By.TAG_NAME, 'li')[2].get_attribute('textContent').split(" ")[1])
        return self.correct_timezone(sdatetime, stimezone), stemperature, shumidity, sprecipitation, swind
    
    def correct_timezone(self, dt, tz):
        if tz == "EAT": tz = "Etc/GMT-3"
        adj_tz = datetime.fromtimestamp(dt/1000.0, timezone(tz)).replace(microsecond=0, tzinfo=None)
        return adj_tz
