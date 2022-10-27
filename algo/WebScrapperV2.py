import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from blueprint import database
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

class ScrapeLazada():

    def scrape(self):
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.binary_location = GOOGLE_CHROME_PATH
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument('--window-size=1920x1480')
        #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        url = 'https://www.lazada.sg/men-sports-clothing-t-shirts/?from=wangpu'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        #time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        products = []
        for item in soup.findAll('div', class_='Bm3ON'):
            product_name = item.find('div', class_='RfADt').text
            price = item.find('span', class_='ooOxS').text
            urlRaw = item.find("div", {"class": "_95X4G"}
                               ).find("a", recursive=False)
            url = urlRaw["href"]
            products.append(
                (product_name, price, url)
            )

        df = pd.DataFrame(products, columns=['Product Name', 'Price', 'URL'])
        df.to_csv('/tmp/test.csv', index=False)
        database.upload('/tmp/test.csv')
        driver.close()



#sl = ScrapeLazada()
#sl.scrape()
