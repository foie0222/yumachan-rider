import io
import json
import os
import re
import base64
import math as m
import requests
from os.path import join, dirname
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv


def create_jpg(entry, ticket_list):
    # ツイートする画像の枚数
    if len(ticket_list) == 0:
        jpg_nums = 1
    else:
        jpg_nums = m.ceil(len(ticket_list) / 33)  # line 1,2,3

    # 画像ファイルを作成
    for jpg_num in range(jpg_nums):
        make_jpg(entry, ticket_list, jpg_num)

    return make_jpg_list(jpg_nums)


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


# 画像に利用するタイトル
def get_title(entry):
    opdt = entry.opdt
    rcoursecd = entry.rcoursecd
    rno = entry.rno
    return opdt + ' ' + convert_to_kanji(rcoursecd) + ' ' + rno + 'R'


# png画像を解析する
def save_png(url):
    file_name = "./image/source.png"

    response = requests.get(url)
    image = response.content

    with open(file_name, "wb") as f:
        f.write(image)


GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='

# 環境変数の読み取り
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_KEY = os.environ.get("GOOGLE_API_KEY")


# APIを呼び、認識結果をjson型で返す
def request_cloud_vison_api(image_base64):
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                # jsonに変換するためにstring型に変換する
                'content': image_base64.decode('utf-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION',  # ここを変更することで分析内容を変更できる
                'maxResults': 10,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()


# jpgリストを返す
def make_jpg_list(jpg_nums):
    jpg_list = []
    for i in range(jpg_nums):
        jpg_list.append('./image/vote_{}.jpg'.format(i))

    return jpg_list


# 画像読み込み
def img_to_base64(filepath):
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.b64encode(img_byte)

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


def trim_result_capture():
    im = Image.open('image/result.png')
    im_crop = im.crop((260, 210, 750, 475))
    im_crop.save('image/tweet_result.png', quality=95)