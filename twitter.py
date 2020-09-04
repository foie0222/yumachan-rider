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


def tweet_with_jpg(entry, jpg_nums):
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
