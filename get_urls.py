
import time
import csv
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


PATH_DRIVER = os.environ['PATH_DRIVER']
URL = os.environ['URL_START']


def get_urls(soup: BeautifulSoup):
    return [j.find('a').get('href') for j in soup.find(id='chats').find_all(class_='link')]


def get_titles(soup: BeautifulSoup):
    return [i.get_text(strip=True) for i in soup.find(id='chats').find_all(class_='card-title')]


def save_csv(urls, titles):
    data = []
    for i, _ in enumerate(urls):
        data.append([urls[i], titles[i]])
    with open('groups_urls.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer_list = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer_list.writerows(data)


def main():
    service = Service(PATH_DRIVER)
    options = ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)

    for i in range(1, 1090):
        time.sleep(0.35)
        driver.get(''.join((URL, str(i))))
        time.sleep(0.35)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        urls = get_urls(soup)
        titles = get_titles(soup)
        save_csv(urls, titles)


if __name__ == '__main__':
    main()
