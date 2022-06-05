import string
import requests
import os
from bs4 import BeautifulSoup


def search(usr_url, temp_article):
    links = []
    r = requests.get(usr_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.findAll('article')
    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'}).text.strip()
        if article_type == temp_article:
            links.append(f"https://nature.com{article.find('a')['href']}")
            # print(article.find('a')['href'])
            # print(article.find('a').get('href'))
    return links


def fetch_data_url(url_):
    content = ''
    page = requests.get(url_, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.find('title').text)
    title = soup.find('title').text
    new_title = "".join([char for char in title if char not in string.punctuation]).replace(" ", "_")
    new_title = f"{new_title}.txt"

    div_all = soup.findAll('div')
    for elem in div_all:
        if elem.has_attr('class'):
            # print(elem['class'])
            if any('body' in i for i in elem['class']):
                content = elem.text.strip()
                # print(content)

    if page.status_code == 200:
        with open(new_title, 'wb') as file:
            file.write(content.encode('utf-8'))
            return new_title
    else:
        return f'The URL returned {page.status_code}!'


if __name__ == '__main__':
    url_template = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
    pages = int(input())
    article_ = input()
    file_list = []
    for i in range(1, pages + 1):
        os.mkdir(f'Page_{i}')
        os.chdir(f'Page_{i}')
        url = f'{url_template}{i}'
        print(url)
        print(article_)
        for link in search(url, article_):
            file_list.append(fetch_data_url(link))
        os.chdir('..')
    print(f'Saved all articles: {file_list}')
