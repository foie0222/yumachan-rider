import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.response = requests.get(url)

    def get_header_txt(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find(
                    "a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(
                target_soup.header.find(
                    "a", class_="entry-title-link bookmark").string)

        return None

    def get_body_txt(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find(
                    "a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(target_soup.find("div", class_="entry-content").p)

        return None

    def get_png_url(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find(
                    "a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(
                target_soup.find(
                    "img",
                    class_="hatena-fotolife")['src'])

    def get_entry_inner_list(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")

        return soup.find_all("div", class_="entry-inner")

    def get_next_url(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")

        return str(
            soup.find(
                "span",
                class_="pager-next").find("a").get("href"))


def isLocal(entry_inner):
    return entry_inner.header.find(
        "a", class_="entry-category-link category-地方競馬") is not None  # 地方競馬ならTrue


def get_date(entry_inner):
    return entry_inner.find(
        "a", class_="entry-title-link bookmark").string[:8]  # レース日付を取得


def get_url(entry_inner):
    return entry_inner.find(
        "a", class_="entry-title-link bookmark").get("href")  # レースのURLを取得
