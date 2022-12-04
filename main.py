
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


def get_urls() -> list:
    with open('groups_urls.csv', 'r', newline='\n', encoding='utf-8') as csvfile:
        reader_csv = csv.reader(csvfile)
        return [[row[0].strip(), row[1].strip()] for row in reader_csv]


def save_csv(dict_: dict) -> None:
    with open('raiting_of_groups.csv', 'a', newline='', encoding='utf-8') as csvfile:
        columns = ['position', 'title', 'url', 'number of members', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writerow(dict_)


def main():
    service = Service(PATH_DRIVER)
    options = ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)

    data = get_urls()[9009:]

    for position, i in enumerate(data, start=9009):
        driver.get(i[0])
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        time.sleep(0.5)

        try:
            number_of_members = soup.find(class_='tgme_page_extra').get_text(strip=True)
            number_of_members = number_of_members.partition('m')[0].strip()
            while ' ' in number_of_members:
                number_of_members = number_of_members.replace(' ', '')
            number_of_members = int(number_of_members)
        except AttributeError:
            number_of_members = "no attribute"
        except ValueError:
            number_of_members = "no members"

        try:
            description = soup.find(class_='tgme_page_description').text
        except AttributeError:
            description = "no attribute"

        dict_ = {
            'position': position,
            'title': i[1],
            'url': i[0],
            'number of members': number_of_members,
            'description': description
        }

        save_csv(dict_)


if __name__ == '__main__':
    main()
