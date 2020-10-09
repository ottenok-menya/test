import re
import mysql.connector
from bs4 import BeautifulSoup
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
    for url in url_list[:2]:
        '''
        Необходимо убрать слайс для парсинга всего сайте
        '''
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
    data = {}
    for url in url_list[:2]:
        html = driver.page_source
        driver.get(url)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.findAll('p')
        for item in items:
            imya = item.find('b')
            text = item.text
            pattern = re.compile("\Цена: \d+")
            cena = pattern.findall(text)
            if len(cena) != 0 and imya != None:
                title = str(imya)[3:-4]
                price = cena[0]
                data.update({title:price})
        sleep(5)
    return(data)


def save_data(json):
    for i, j in zip(json.keys(), json.values()):
        connection = mysql.connector.connect(host='localhost',
                                             user='ulan',
                                             password='password',
                                             database='books')
        cursor = connection.cursor()
        insert_query = '''INSERT INTO books(title, price) VALUES(%s, %s)'''
        record = (i, j)
        cursor.execute(insert_query, record)
        connection.commit()
        print('Success')

    cursor.close()

save_data(get_data(get_all_pages(get_all_categories(html))))

