import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from scrapper_to_firebase import upload,download_csv,start_stream

class ScrapeLazada():

    def scrape(self,url):
        
        #chrome_options= webdriver.ChromeOptions()
        #chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--no-sandbox")
        #driver = webdrive.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        #driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
        #url = 'https://www.lazada.sg/men-sports-clothing-t-shirts/?under-armour&from=wangpu'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        print(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        df = pd.DataFrame()
        products = []
        for item in soup.findAll('div', class_='Bm3ON'):
            urlRaw = item.find("div", {"class": "_95X4G"}
                               ).find("a", recursive=False)
            url = "https:" + urlRaw["href"]
            df = self.call(url, df)
        print(df)
        df.to_csv("testscrape.csv", index=False)        
        with open('main_dataset.csv','a') as f:
            df.to_csv(f, index=False)
        upload('main_dataset.csv','main_dataset.csv')
        driver.close()

    def call(self, url, df):
        urlNew = url
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(urlNew)

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []

        results = list(map(int, filter(None, [i.text for i in soup.find_all(
            'button', {'class': 'next-pagination-item'})])))

        if results:

            for i in range(max(results)+1):

                for item in soup.find('div', class_='mod-reviews').find_all('div', class_='item'):

                    stars = len(item.find('div', class_='top').find_all('img'))
                    _by = item.find('div', class_='middle').find('span').text
                    startList = [stars, _by]
                    for details in soup.findAll('li', class_='key-li'):
                        temp = details.find('div', class_='key-value').text
                        startList.append(temp)
                    products.append(startList)
                time.sleep(2)
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "button.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next").click()
                except:
                    break
                time.sleep(3)

        newdf = df.append(products)
        return newdf
        
    def scrape_single_item(self,url):
        
        #chrome_options= webdriver.ChromeOptions()
        #chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--no-sandbox")
        #driver = webdrive.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        #driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
        #url = 'https://www.lazada.sg/men-sports-clothing-t-shirts/?under-armour&from=wangpu'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)
        print(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        df = pd.DataFrame()
        products = []
        for item in soup.findAll('div', class_='Bm3ON'):
            urlRaw = item.find("div", {"class": "_95X4G"}
                               ).find("a", recursive=False)
            url = "https:" + urlRaw["href"]
            df = self.call(url, df)
            break
        print(df)
        df.to_csv("testscrape.csv", index=False)        
        with open('main_dataset.csv','a') as f:
            df.to_csv(f, index=False)
        upload('main_dataset.csv','main_dataset.csv')
        driver.close()

sl = ScrapeLazada()
#start_stream() #start to read crawl lists from database and write a crawl_lists.txt
try:
    with open("crawl_lists.txt") as f: #try to read in crawl_lists.txt
        contents = f.read()
        lists_of_details = contents.split("\n")
        print(lists_of_details)
        for item in lists_of_details:
            if item != "":
                url = item.split(",")[0]
                mode = item.split(",")[1]
                if mode == "single_page":
                    print("page mode")
                    sl.scrape(url)                
                    #download_csv()                
                elif mode == "single_item":
                    print("single mode")               
                    #download_csv()   
                    sl.scrape_single_item(url)
except FileNotFoundError as e:
    print(e)
    print("crawl stop")