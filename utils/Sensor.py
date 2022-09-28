from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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
        conditions = self.driver.find_element(By.XPATH, '//div[@class="col-6 pb-20 pl-50"]')

        humidity, precipitation, wind = self.parse_data(conditions)
        print(f"Humidity: {humidity}\nPrecipitation: {precipitation}\nWind: {wind}")
    
    def parse_data(self, conditions):
        humidity = int(conditions.find_elements(By.TAG_NAME, 'li')[0].get_attribute('textContent').split(" ")[1][0:-1])
        precipitation = int(conditions.find_elements(By.TAG_NAME, 'li')[1].get_attribute('textContent').split(" ")[1][0:-1])
        wind = float(conditions.find_elements(By.TAG_NAME, 'li')[2].get_attribute('textContent').split(" ")[1])
        
        return humidity, precipitation, wind
