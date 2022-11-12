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
    def crawlWholeStore(self, url, projectName):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 1080)")

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        results = list(map(int, filter(None, [i.text for i in soup.find_all(
            'li', {'class': 'ant-pagination-item'})])))
        df = pd.DataFrame()
        df2 = pd.DataFrame()
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
                    url2 = "https:" + urlRaw["href"]
                    df = self.intoPageToGetReview(url2, df)
                    df2 = self.intoPageToGetProductDetails(url2, df2)
                    print(df2)
                time.sleep(2)
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "button.ant-pagination-item-link").click()
                except:
                    break
                time.sleep(3)

        fileName = projectName + ".csv"
        df2.to_csv(fileName, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        df.to_csv('main_datasetBackup.csv', mode='a', index=False, header=False)
        df3 = pd.read_csv('main_dataset.csv', on_bad_lines='skip', names=['0','1','2','3','4','5','6','7'])
        df3.drop_duplicates(subset=['0','1','2','3','4','5','6','7'], keep=False)
        df3.to_csv('main_dataset.csv', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(fileName,fileName)
        driver.close()

    def intoPageToGetProductDetails(self, url, df):
        urlNew = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(urlNew)
        driver.execute_script("window.scrollTo(0, 1080)")

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []
        startList = []
        title = soup.find('h1', class_='pdp-mod-product-badge-title').text
        startList.append(title)
        for details in soup.findAll('li', class_='key-li'):
            temp = details.find('div', class_='key-value').text
            startList.append(temp)
        products.append(startList)

        newdf = df.append(products)
        return newdf

    # For Url that will only scrape the first page it sees

    def scrapeOnePage(self, url, projectName):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
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

        fileName = projectName + ".csv"
        df2.to_csv(fileName, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)     
        df.to_csv('main_datasetBackup.csv', mode='a', index=False, header=False)
        df3 = pd.read_csv('main_dataset.csv', on_bad_lines='skip', names=['0','1','2','3','4','5','6','7'])
        df3.drop_duplicates(subset=['0','1','2','3','4','5','6','7'], keep=False)
        df3.to_csv('main_dataset.csv', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(fileName,fileName)        
        driver.close()

    def intoPageToGetReview(self, url, df):
        urlNew = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
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
    def singleProductPage(self, url, projectName):
        urlNew = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
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
        df2 = pd.DataFrame()
        df2 = self.intoPageToGetProductDetails(urlNew, df2)
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
                
        if not results:

            for item in soup.find('div', class_='mod-reviews').find_all('div', class_='item'):

                stars = len(item.find('div', class_='top').find_all('img'))
                _by = item.find('div', class_='middle').find('span').text
                startList = [stars, _by]
                for details in soup.findAll('li', class_='key-li'):
                    temp = details.find('div', class_='key-value').text
                    startList.append(temp)
                products.append(startList)
                
                time.sleep(2)

        df = df.append(products)
        fileName = projectName + ".csv"
        df2.to_csv(fileName, index=False)
        df.to_csv('main_dataset.csv', mode='a', index=False, header=False)
        df.to_csv('main_datasetBackup.csv', mode='a', index=False, header=False)
        df3 = pd.read_csv('main_dataset.csv', on_bad_lines='skip', names=['0','1','2','3','4','5','6','7'])
        df3.drop_duplicates(subset=['0','1','2','3','4','5','6','7'], keep=False)
        df3.to_csv('main_dataset.csv', index=False, header=False)
        upload('main_dataset.csv','main_dataset.csv')
        upload(fileName,fileName)
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
                projectName = item.split(",")[2]
                if mode == "whole_page":         
                    download_csv()  
                    print("whole page mode")
                    sl.scrape(url,projectName)       
                if mode == "single_page":
                    print("single page mode")                
                    download_csv()                           
                    sl.singlePage(url,projectName)
                elif mode == "single_item":               
                    download_csv()   
                    print("single mode")
                    sl.singleProductPage(url,projectName)
                os.remove(projectName+".csv")
except FileNotFoundError as e:
    print(e)
    print("crawl stop")
#sl.singleProductPage("https://www.lazada.sg/products/under-armour-ua-mens-tech-20-short-sleeve-i2268365191-s13395451241.html?clickTrackInfo=query%253A%253Bnid%253A2268365191%253Bsrc%253AlazadaInShopSrp%253Brn%253Ab0e26f5873c4cad28d52128b87401682%253Bregion%253Asg%253Bsku%253A2268365191_SGAMZ%253Bprice%253A35.00%253Bclient%253Adesktop%253Bsupplier_id%253A1000259426%253Basc_category_id%253A4861%253Bitem_id%253A2268365191%253Bsku_id%253A13395451241%253Bshop_id%253A349621&freeshipping=1&fs_ab=1&fuse_fs=1&mp=1&spm=a2o42.seller.list.i40.6a6d2d4dFfvsy4", "newproject")
# sl.scrape()
#sl.crawlWholeStore(
    #"https://www.lazada.sg/men-sports-clothing-t-shirts/?under-armour&from=wangpu", "project1")
