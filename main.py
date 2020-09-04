from gss import write_gss
from odds import get_realtime_odds
from scraper import Scraper, get_date, get_url, isLocal
from entry import get_entry
from ticket import make_ticket
from writer import make_csv, write_races_csv, write_result_to_csv
from verification import get_verification_list
from ipatgo import vote
from twitter import tweet_with_jpg
from images import create_jpg
from slack import send_slack
import sys
import time
import glob

# データを取得する対象
URL = "https://www.ai-yuma.com/"


def main():
    timestamp = sys.argv[1]

    # ゆまちゃんのHRから情報を取得
    scraper = Scraper(URL)
    header_txt = scraper.get_header_txt()
    body_txt = scraper.get_body_txt()

    # 取得した結果を変換
    entry = get_entry(header_txt, body_txt)

    # リアルタイムオッズを取得
    realtime_odds = get_realtime_odds(entry.opdt, entry.rcoursecd, entry.rno)

    # 購入馬券リストを作る
    ticket_list = make_ticket(entry, realtime_odds)

    # 購入馬券リストをcsvに書き出す
    make_csv(ticket_list, timestamp)

    # ipatgoで投票
    vote(timestamp)

    # 買い目画像作成
    jpgs = create_jpg(entry, ticket_list)

    # スラック通知
    send_slack(jpgs)

    # tweet
    tweet_with_jpg(entry, len(jpgs))

    # 購入馬券リストをGSSに書き出す
    write_gss(ticket_list, timestamp, True)


def verify():
    date_list = ['races/202005*.txt']
    for date in date_list:
        file_list = sorted(glob.glob(date), reverse=False)
        for target_file in file_list:
            all_verification_list = []
            with open(target_file) as lines:
                for line in lines:
                    URL = line.rstrip()

                    # ゆまちゃんのHRから情報を取得
                    scraper = Scraper(URL)
                    header_txt = scraper.get_header_txt()
                    body_txt = scraper.get_body_txt()

                    # 「本日の結果」だったらスキップ
                    if '結果' in header_txt:
                        continue

                    # 取得した結果を変換
                    entry = get_entry(header_txt, body_txt)

                    # リアルタイムオッズを取得
                    realtime_odds = get_realtime_odds(
                        entry.opdt, entry.rcoursecd, entry.rno)

                    # # 購入馬券リストを作る
                    ticket_list = make_ticket(entry, realtime_odds)

                    # 検証用のデータを作成
                    verification_list = get_verification_list(ticket_list)

                    for verification in verification_list:
                        print(verification.to_string())

                    # csv書き出し
                    write_result_to_csv(entry.opdt, verification_list)

                    all_verification_list.extend(verification_list)

            all_bet = 0
            all_refund = 0
            tan_bet = 0
            tan_refund = 0
            fuku_bet = 0
            fuku_refund = 0
            wide_bet = 0
            wide_refund = 0
            trio_bet = 0
            trio_refund = 0
            for verification in all_verification_list:
                if verification.ticket.denomination == 'TANSYO':
                    tan_bet += int(verification.ticket.bet_price)
                    tan_refund += int(verification.ticket.bet_price) * \
                        verification.refund / 100

                if verification.ticket.denomination == 'FUKUSYO':
                    fuku_bet += int(verification.ticket.bet_price)
                    fuku_refund += int(verification.ticket.bet_price) * \
                        verification.refund / 100

                if verification.ticket.denomination == 'WIDE':
                    wide_bet += int(verification.ticket.bet_price)
                    wide_refund += int(verification.ticket.bet_price) * \
                        verification.refund / 100

                if verification.ticket.denomination == 'TRIO':
                    trio_bet += int(verification.ticket.bet_price)
                    trio_refund += int(verification.ticket.bet_price) * \
                        verification.refund / 100

                all_bet += int(verification.ticket.bet_price)
                all_refund += int(verification.ticket.bet_price) * \
                    verification.refund / 100

            print('opdt is       ', entry.opdt)
            print('all_bet is    ', '{:.0f}'.format(all_bet))
            print('all_refund is ', '{:.0f}'.format(all_refund))
            print('tan_bet is    ', '{:.0f}'.format(tan_bet))
            print('tan_refund is ', '{:.0f}'.format(tan_refund))
            print('fuku_bet is    ', '{:.0f}'.format(fuku_bet))
            print('fuku_refund is ', '{:.0f}'.format(fuku_refund))
            print('wide_bet is    ', '{:.0f}'.format(wide_bet))
            print('wide_refund is ', '{:.0f}'.format(wide_refund))
            print('trio_bet is    ', '{:.0f}'.format(trio_bet))
            print('trio_refund is ', '{:.0f}'.format(trio_refund))
            print('')
            print('')


# 検証のためのURLを取得するためのロジック
def url_scrape(loop):
    url = URL
    count = 0
    while count < loop:

        scraper = Scraper(url)
        entry_inner_list = scraper.get_entry_inner_list()

        for entry_inner in entry_inner_list:
            if isLocal(entry_inner):  # 地方競馬ならスキップ
                continue
            date = get_date(entry_inner)  # like 20200330
            url = get_url(entry_inner)  # レースのURL
            write_races_csv(date, url)  # csv書き出し
            time.sleep(3)  # 次のループまで3秒待つ

        url = scraper.get_next_url()
        count += 1


if __name__ == '__main__':
    if sys.argv[1] == 'verification':
        verify()
    elif sys.argv[1] == 'scraping':
        url_scrape(int(sys.argv[2]))  # ループを回したい回数
    else:
        main()
