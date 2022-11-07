
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

    # For Url to crawl every Item page on their store
    def crawlWholeStore(self, url,projectid):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 1080)")

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        results = list(map(int, filter(None, [i.text for i in soup.find_all(
            'li', {'class': 'ant-pagination-item'})])))
        df = pd.DataFrame()
        products = []
        if results:
            counter = 1
            for i in range(max(results)+1):
                options = webdriver.ChromeOptions()
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
                driver = webdriver.Chrome(options=options)
                newUrl = url + "&Page=" + str(counter)
                driver.get(newUrl)
                driver.execute_script("window.scrollTo(0, 1080)")

                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, "html.parser")

                df = pd.DataFrame()
                for item in soup.findAll('div', class_='Bm3ON'):
                    urlRaw = item.find("div", {"class": "_95X4G"}
                                       ).find("a", recursive=False)
                    url = "https:" + urlRaw["href"]
                    df = self.intoPageToGetReview(url, df)

        project_name = projectid+".csv"
        df.to_csv(project_name, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(project_name,project_name)
        driver.close()

    # For Url that will only scrape the first page it sees

    def scrapeOnePage(self, url,projectid):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 1080)")

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
            df = self.intoPageToGetReview(url, df)

        project_name = projectid+".csv"
        df.to_csv(project_name, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(project_name,project_name)
        driver.close()

    def intoPageToGetReview(self, url, df):
        urlNew = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(urlNew)
        driver.execute_script("window.scrollTo(0, 1080)")

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

    # when URL is only for 1 product
    def singleProductPage(self, url,projectid):
        urlNew = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(urlNew)
        driver.execute_script("window.scrollTo(0, 1080)")

        WebDriverWait(driver, 10).until(
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
        project_name = projectid+".csv"
        df.to_csv(project_name, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(project_name,project_name)
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
                projectid = item.split(",")[2]
                if mode == "whole_page":         
                    download_csv()  
                    print("whole page mode")
                    sl.scrape(url,projectid)       
                if mode == "single_page":
                    print("single page mode")                
                    download_csv()                           
                    sl.singlePage(url,projectid)
                elif mode == "single_item":               
                    download_csv()   
                    print("single mode")
                    sl.singleProductPage(df,url,projectid)
except FileNotFoundError as e:
    print(e)
    print("crawl stop")
# sl.scrape()
#sl.crawlWholeStore(
    "https://www.lazada.sg/men-sports-clothing-t-shirts/?under-armour&from=wangpu")
