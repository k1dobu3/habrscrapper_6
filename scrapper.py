import sqlite3
import json
import requests
from bs4 import BeautifulSoup
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.4.864 Yowser/2.5 Safari/537.36"
}
url = 'https://habr.com/ru/flows/develop/'
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('article', class_='tm-articles-list__item')
news_dict = {}

def scraper():
  for n, i in enumerate(quotes, start=1):
    # try/except исключает возможность пустого пользователям в статьях от самого портала Habr
    try:
        itemUser = i.find('a', class_='tm-user-info__username').text.strip()
    except:
        itemUser = 'Habr'
    itemName = i.find('h2').text
    itemTagsNoneFormat = i.find('div', class_='tm-publication-hubs')  # tags
    itemTagsNoneFullFormat = itemTagsNoneFormat.get_text()
    itemTags = itemTagsNoneFullFormat.replace('*', '')
    itemDescr = i.find('div', class_='article-formatted-body').text.strip()
    itemUrl = f"https://habr.com{i.find('a', class_='tm-title__link', href=True).get('href')}"
    itemUserUrl = f"https://habr.com{i.find('a', href=True).get('href')}"
    itemId = itemUrl.split('/')[-2]

    news_dict[itemId] = {
        "itemName": itemName,
        "itemUser": itemUser,
        "itemTags": itemTags,
        "itemDescr": itemDescr,
        "itemUrl": itemUrl,
        "itemUserUrl": itemUserUrl
    }
  
  with open("news_dict.json", "w") as file:
      json.dump(news_dict, file, indent=4, ensure_ascii=False)
  print("Парсер отработал")


def main():
  scrapper()


if __name__ == '__main__':
    main()
