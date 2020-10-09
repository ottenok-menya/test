from bs4 import BeautifulSoup
import re

from django.contrib.sites import requests
from selenium import webdriver
from time import sleep

url = 'http://www.alib.ru/kat.phtml'
driver = webdriver.Chrome()
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')


def get_all_categories(html):
    items = soup.find('table', {'cellspacing': '20'}).findAll('li')
    categories = []
    links = []

    for item in items:
        category = item.get_text().strip()
        category = re.sub(r'\d\ ·.+', '', category)
        categories.append(category)
        link = item.find('a')
        links.append(link.attrs['href'])
    return links


def get_all_pages(url_list):
    all_pages = []
    for url in url_list:
        html = driver.page_source
        driver.get(url)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.findAll('b')
        for item in items:
            try:
                pages = item.findAll('a')
            except Exception:
                pass
            for page in pages:
                all_pages.append("https:"+page.attrs['href'])
        sleep(5)
    return all_pages


def get_data(url_list):
    for url in url_list:
        link = requests.get(url)
        soup = BeautifulSoup(link, 'lxml')
        items = soup.findAll('p').text
        print(items)


get_data(get_all_pages(get_all_categories(html)))

