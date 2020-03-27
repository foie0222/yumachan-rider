from odds import get_realtime_odds
from scraper import Scraper
from entry import get_entry
from ticket import make_ticket
from writer import make_csv
import sys

# データを取得する対象
url = "https://www.ai-yuma.com/"


def main():
    timestamp = sys.argv[1]

    # ゆまちゃんのHRから情報を取得
    scraper = Scraper(url)
    header_txt = scraper.get_get_header_txt()
    body_txt = scraper.get_get_body_txt()

    # 取得した結果を変換
    entry = get_entry(header_txt, body_txt)

    # リアルタイムオッズを取得
    realtime_odds = get_realtime_odds(entry.opdt, entry.rcourcecd, entry.rno)

    # 購入馬券リストを作る
    ticket_list = make_ticket(entry, realtime_odds)

    # 購入馬券リストをcsvに書き出す
    make_csv(ticket_list, timestamp)


if __name__ == '__main__':
    main()
