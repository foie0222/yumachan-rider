import time
import sys
import chromedriver_binary
import os
import subprocess
import io
import re
import base64
from os.path import join, dirname
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import request as rq
from selenium.webdriver import Chrome, ChromeOptions
from PIL import Image, ImageDraw, ImageFont
import math as m

# 環境変数の読み取り
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TWITTER_ID = os.environ.get("TWITTER_ID")
TWITTER_PW = os.environ.get("TWITTER_PW")


def tweet_with_jpg(entry, ticket_list):
    # ツイートする画像の枚数
    if len(ticket_list) == 0:
        jpg_nums = 1
    else:
        jpg_nums = m.ceil(len(ticket_list) / 33)  # line 1,2,3

    # 画像ファイルを作成
    for jpg_num in range(jpg_nums):
        make_jpg(entry, ticket_list, jpg_num)

    try:
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

        # jpgファイルを枚数分アップロード
        for jpg_num in range(jpg_nums):
            file_upload(driver, jpg_num)

        # ツイート
        send_tweet(driver)
        time.sleep(10)

    except Exception as e:
        print(e.args)

    driver.quit()


def file_upload(driver, jpg_num):
    if os.name == 'posix':
        # 入力
        elem = driver.find_element_by_class_name(
            'public-DraftStyleDefault-block')
        subprocess.run(
            ["osascript",
             "-e",
             'set the clipboard to (read (POSIX file "./image/vote_' +
             str(jpg_num) +
             '.jpg") as JPEG picture)'])
        # 画像をペースト
        elem.send_keys(Keys.SHIFT, Keys.INSERT)

    if os.name == 'nt':
        driver.execute_script("window.open()")  # 新規タブ
        driver.switch_to.window(driver.window_handles[1])  # スイッチ
        driver.get(
            'file:///C:/develop/git/yumachan-rider/image/vote_' +
            str(jpg_num) +
            '.jpg')
        elem = driver.find_element_by_tag_name('body')
        elem.send_keys(Keys.CONTROL, 'c')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        elem = driver.find_element_by_class_name(
            'public-DraftStyleDefault-block')
        elem.send_keys(Keys.CONTROL, "v")


# Twitter投稿用のjpgファイルを作成
def make_jpg(entry, ticket_list, jpg_num):
    # base64化された画像データを用意
    data = get_base64('./image/template.jpg')
    image_data_bytes = get_image_data_bytes(data)

    # バイト列をbase64としてデコード
    image_data = base64.b64decode(image_data_bytes)

    # ファイルとして開き、pillowのImageインスタンスにする
    im = Image.open(io.BytesIO(image_data))
    draw = ImageDraw.Draw(im)

    # フォント
    bfnt = ImageFont.truetype('./font/MEIRYOB.TTC', 108)
    nofnt = ImageFont.truetype('./font/MEIRYO.TTC', 64)
    fnt = ImageFont.truetype('./font/MEIRYO.TTC', 72)
    white = (255, 255, 255)

    # タイトル描画
    title = get_title(entry)
    draw.text((100, 100), title, fill=white, font=bfnt)

    # 内容描画
    if len(ticket_list) == 0:
        txt = 'Kidnap the cow instead of betting'
        draw.text((660, 700), txt, fill=white, font=nofnt)
    else:
        for index, ticket in enumerate(
                ticket_list[33 * jpg_num:33 * (jpg_num + 1)]):
            index += 1
            txt = ticket.to_twitter_format()

            q = index // 11
            mod = index % 11

            draw.text((100 + (q if mod != 0 else q - 1) * 820,
                       200 + (index - q * 11 if mod != 0 else 11) * 100),
                      txt,
                      fill=white, font=fnt)

    im.save('./image/vote_' + str(jpg_num) + '.jpg')


def get_image_data_bytes(data):
    return re.sub('^data:image/.+;base64,', '', data).encode('utf-8')


def get_base64(img_file):
    b64 = base64.encodestring(open(img_file, 'rb').read())
    return b64.decode('utf8')


def send_tweet(driver):
    elem = driver.find_element_by_class_name(
        'public-DraftStyleDefault-block')
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


# 画像に利用するタイトル
def get_title(entry):
    opdt = entry.opdt
    rcoursecd = entry.rcoursecd
    rno = entry.rno
    return opdt + ' ' + convert_to_kanji(rcoursecd) + ' ' + rno + 'R'


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
