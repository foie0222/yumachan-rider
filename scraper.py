import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.response = requests.get(url)

    def get_get_header_txt(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find("a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(target_soup.header.find("a", class_="entry-title-link bookmark").string)

        return None

    def get_get_body_txt(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soup = soup.find("div", class_="entry-inner")

        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find("a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(target_soup.find("div", class_="entry-content").p)

        return None
