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

        #url = 'https://www.lazada.sg/men-sports-clothing-t-shirts/?under-armour&from=wangpu'
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")
        WebDriverWait(driver, 5).until(
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

        #df.to_csv("v1.csv", index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        driver.close()

    def call(self, url, df):
        urlNew = url
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        driver = webdriver.Chrome(options=options)
        driver.get(urlNew)
        driver.execute_script("window.scrollTo(0,1080)")
        
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

    def singlePage(self, url):
        urlNew = url
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(urlNew)
        driver.execute_script("window.scrollTo(0,1080)")

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []
        results = list(map(int, filter(None, [i.text for i in soup.find_all(
            'button', {'class': 'next-pagination-item'})])))
        df = pd.DataFrame()
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

        df = df.append(products)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        driver.close()


sl = ScrapeLazada()
start_stream() #start to read crawl lists from database and write a crawl_lists.txt
try:
    with open("crawl_lists.txt") as f: #try to read in crawl_lists.txt
        contents = f.read()
        lists_of_details = contents.split("\n")
        print(lists_of_details)
        for item in lists_of_details:
            if item != "":
                url = item.split(",")[0]
                print(url)
                mode = item.split(",")[1]
                if mode == "whole_page":         
                    download_csv()  
                    print("whole page mode")
                    sl.scrape(url)       
                if mode == "single_page":
                    print("single page mode")                
                    #download_csv()                           
                    sl.singlePage(url)
                elif mode == "single_item":               
                    download_csv()   
                    print("single mode")
                    df = pd.DataFrame()
                    df = sl.call(df,url)
                    df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
                    upload('main_dataset.csv','main_dataset.csv')
except FileNotFoundError as e:
    print(e)
    print("crawl stop")
# sl.scrape()
#sl.singlePage("https://www.lazada.sg/products/under-armour-ua-mens-performance-apparel-short-sleeve-i2012723227-s10952881051.html?clickTrackInfo=query%253A%253Bnid%253A2012723227%253Bsrc%253AlazadaInShopSrp%253Brn%253A7ea1e9db1436f1bd52388f7e99dfe0b4%253Bregion%253Asg%253Bsku%253A2012723227_SGAMZ%253Bprice%253A23.40%253Bclient%253Adesktop%253Bsupplier_id%253A1000259426%253Basc_category_id%253A4861%253Bitem_id%253A2012723227%253Bsku_id%253A10952881051%253Bshop_id%253A349621&freeshipping=1&fs_ab=1&fuse_fs=1&mp=1&spm=a2o42.seller.list.i40.6a6d2d4dq39QTv")
