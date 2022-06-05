from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://www.azmovies.net'
def get_html(url):
    response = requests.get(url)
    return response.text


list2 = []


def get_info(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find_all("div", class_="listinfo")
    for i in info:
        h2 = i.find('h2').text
        # print(h2)
        a = i.find('a').get('href')
        # print(a)
        all = f"🎬 {h2}   *** link to the video 📺 ->  {a}"
        list2.append(all)
    # print(list2)
    return list2



get_info(get_html(BASE_URL))
