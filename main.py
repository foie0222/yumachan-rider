from scraper import Scraper
from entry import get_entry
from ticket import make_ticket
from writer import make_csv

# データを取得する対象
url = "https://www.ai-yuma.com/?page=1584683595"


def main():

    scraper = Scraper(url)
    header_txt = scraper.get_get_header_txt()
    body_txt = scraper.get_get_body_txt()
    entry = get_entry(header_txt, body_txt)

    ticket_list = make_ticket(entry)

    make_csv(ticket_list)


if __name__ == '__main__':
    main()
