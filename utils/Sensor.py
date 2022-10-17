from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pytz import timezone
from datetime import datetime


class Sensor:
    def __init__(self, name, url, stimezone):
        self.name = name
        self.url = url
        self.stimezone = stimezone
    
    def configure_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("lvog-level=1")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(10)
        return driver

    def get_data(self, soutput, plog=False):
        driver = self.configure_driver()
        driver.get(self.url)
        thermal = driver.find_element(By.XPATH, '//div[@class="col-6 pb-20"]')
        conditions = driver.find_element(By.XPATH, '//div[@class="col-6 pb-20 pl-50"]')
        sdatetime, stemperature, shumidity, sprecipitation, swind = self.parse_data(conditions, thermal)
        sid = (f"{self.name}+{sdatetime}")
        if plog: print(f"Datetime: {sdatetime}\nTemperature: {stemperature}\nHumidity: {shumidity}\nPrecipitation: {sprecipitation}\nWind: {swind}")
        soutput.append((sid, sdatetime, stemperature, shumidity, sprecipitation, swind))
        driver.quit()

    def parse_data(self, conditions, thermal):
        stemperature = int(thermal.find_elements(By.TAG_NAME, 'li')[1].get_attribute('textContent').split("°")[0])
        sdatetime = float(thermal.find_elements(By.TAG_NAME, 'li')[0].get_attribute('innerHTML').split("\"")[1])
        shumidity = int(conditions.find_elements(By.TAG_NAME, 'li')[0].get_attribute('textContent').split(" ")[1][0:-1])
        sprecipitation = int(conditions.find_elements(By.TAG_NAME, 'li')[1].get_attribute('textContent').split(" ")[1][0:-1])
        swind = float(conditions.find_elements(By.TAG_NAME, 'li')[2].get_attribute('textContent').split(" ")[1])
        return self.correct_timezone(sdatetime), stemperature, shumidity, sprecipitation, swind
    
    def correct_timezone(self, dt):
        adj_tz = datetime.fromtimestamp(dt/1000.0, timezone(self.stimezone.replace('+', '%temp%').replace('-', '+').replace('%temp%', '-')))
        return adj_tz.strftime('%d-%m-%Y_%H-%M-00')
