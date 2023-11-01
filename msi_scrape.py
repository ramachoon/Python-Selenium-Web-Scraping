import os
import pandas as pd
import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

home_url = "https://msi.hsu.edu.hk"

driver = webdriver.Chrome()
driver.get("https://msi.hsu.edu.hk/en/news-and-announcement")
time.sleep(5)
WebDriverWait(driver, 20)
li_elements=driver.find_elements(By.XPATH,'//div[@class="paginationjs-pages"]/ul/li')
# li_elements = driver.find_elements_by_css_selector('.paginationjs-page')

largest_data_num = 1

# pg_num=len(liobjects)

# Loop through the li elements and compare the data-num values
for li_element in li_elements:
    # Get the value of the data-num attribute
    data_num = li_element.get_attribute('data-num')
    if(data_num):
        # Convert the data-num value to an integer
        data_num = int(data_num)

        # Compare the data-num value with the current largest value
        if data_num > largest_data_num:
            largest_data_num = data_num

# The largest_data_num variable now contains the largest data-num value
print(largest_data_num)

newsList = []

for page in range(1,largest_data_num+1):
 
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="paginationjs-pages"]/ul/li[@data-num='+str(page)+']'))).click()
    print(page)
    WebDriverWait(driver, 40)
    time.sleep(5)
    news_ten=driver.find_elements(By.XPATH,'//div[@data-title="Loading ..."]/div')
    news_container=driver.find_element(By.XPATH,'//div[@data-title="Loading ..."]')
    # print(news_ten.get_attribute("innerHTML"))

    for news_index in range(1,len(news_ten)+1):
        title = ''
        newsUrl = ''
        featuredImgUrl = ''
        date = ''
        try:
            featuredImgUrl = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div[1]/div/a/img').get_attribute('src')
            title = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div[2]/div/h3/a').text
            newsUrl = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div[2]/div/h3/a').get_attribute('href')
            date = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div[2]/div/div[1]/span').text.strip()
        except NoSuchElementException:
            title = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div/div/h3/a').text
            newsUrl = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div/div/h3/a').get_attribute('href')
            featuredImgUrl = ''
            date = news_container.find_element(By.XPATH,'./div['+str(news_index)+']/div/div/div/div/div[1]/span').text.strip()
        if newsUrl.find('http') == -1:
            newsUrl = home_url + newsUrl
        if featuredImgUrl.find('http') == -1 and  featuredImgUrl != '':
            featuredImgUrl = home_url + featuredImgUrl
        newsList.append({"title":title, "url": newsUrl, "featuredImgUrl": featuredImgUrl, "date": date })
    WebDriverWait(driver, 40)
    time.sleep(5)

for newsItem in newsList:
    driver.get(newsItem['url'])
    time.sleep(5)
    WebDriverWait(driver, 20)
    li_elements = driver.find_elements(By.XPATH,'//div[@class="paginationjs-pages"]/ul/li')


    
print(newsList)

time.sleep(5)
driver.quit()