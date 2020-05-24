import time
import sys
import chromedriver_binary
import os
import subprocess
import io
import re
import base64
import win32clipboard
from os.path import join, dirname
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import request as rq
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageDraw, ImageFont

# 環境変数の読み取り
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TWITTER_ID = os.environ.get("TWITTER_ID")
TWITTER_PW = os.environ.get("TWITTER_PW")


def tweet_with_jpg(entry, ticket_list):
    try:
        # 画像ファイルを作成
        make_jpg(entry, ticket_list)

        # オプション追加
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        driver = get_webdriver(options)

        TWITTER_LOGIN_URL = "https://twitter.com/login"
        driver.get(TWITTER_LOGIN_URL)

        time.sleep(1)
        id = driver.find_element_by_name('session[username_or_email]')
        id.send_keys(TWITTER_ID)

        password = driver.find_element_by_name('session[password]')
        password.send_keys(TWITTER_PW)

        # ログイン
        password.send_keys(Keys.ENTER)
        time.sleep(1)

        # 入力
        elem = driver.find_element_by_class_name(
            'public-DraftStyleDefault-block')

        # 画像ファイルをクリップボードにコピー
        copy_to_clipboard()

        # 画像をペースト
        elem.send_keys(Keys.SHIFT, Keys.INSERT)

        # ツイート
        send_tweet(elem)
        time.sleep(3)

    except Exception as e:
        print(e.args)

    driver.quit()


def make_jpg(entry, ticket_list):
    # base64化された画像データを用意
    data = get_base64('./image/template.jpg')

    # 頭のいらない部分を取り除いた上で、バイト列にエンコード
    image_data_bytes = re.sub(
        '^data:image/.+;base64,',
        '',
        data).encode('utf-8')

    # バイト列をbase64としてデコード
    image_data = base64.b64decode(image_data_bytes)

    # ファイルとして開き、pillowのImageインスタンスにする
    im = Image.open(io.BytesIO(image_data))
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('./font/MEIRYO.TTC', 18)

    # テキスト作成
    opdt = entry.opdt
    rcoursecd = entry.rcoursecd
    rno = entry.rno
    title = opdt + ' ' + convert_to_kanji(rcoursecd) + ' ' + rno + 'R'

    content = title + '\n'
    if len(ticket_list) == 0:
        content = content + '買い目なし'
    else:
        for ticket in ticket_list:
            content = content + ticket.to_twitter_format() + '\n'
    draw.text((5, 0), content, font=fnt)
    im.save("./image/vote.jpg")


def copy_to_clipboard():
    data = get_base64('./image/vote.jpg')
    if os.name == 'nt':
        send_to_clipboard(win32clipboard.CF_DIB, data)

    if os.name == 'posix':
        subprocess.run(
            ["osascript",
             "-e",
             'set the clipboard to (read (POSIX file "./image/vote.jpg") as JPEG picture)'])


def send_to_clipboard(clip_type, data):
    # クリップボードをクリアして、データをセットする
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def send_tweet(elem):
    if os.name == 'nt':
        elem.send_keys(Keys.CONTROL, Keys.ENTER)

    if os.name == 'posix':
        elem.send_keys(Keys.COMMAND, Keys.ENTER)


def get_webdriver(options):
    if os.name == 'nt':
        return webdriver.Chrome(
            options=options,
            executable_path='./driver/chromedriver.exe')

    if os.name == 'posix':
        return webdriver.Chrome(
            options=options,
            executable_path='./driver/chromedriver')

    return None


def convert_to_kanji(txt):
    if 'SAPPORO' in txt:
        return '札幌'
    if 'HAKODATE' in txt:
        return '函館'
    if 'FUKUSHIMA' in txt:
        return '福島'
    if 'NIIGATA' in txt:
        return '新潟'
    if 'TOKYO' in txt:
        return '東京'
    if 'NAKAYAMA' in txt:
        return '中山'
    if 'CHUKYO' in txt:
        return '中京'
    if 'KYOTO' in txt:
        return '京都'
    if 'HANSHIN' in txt:
        return '阪神'
    if 'KOKURA' in txt:
        return '小倉'


def get_base64(img_file):
    b64 = base64.encodestring(open(img_file, 'rb').read())
    return b64.decode('utf8')
