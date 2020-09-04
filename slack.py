import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数の読み取り
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL = os.environ.get('CHANNEL')


def send_slack(jpgs):
    for i in range(len(jpgs)):
        upload_files(jpgs, i)


def upload_files(jpgs, jpg_num):
    files = {'file': open(jpgs[jpg_num], 'rb')}
    param = {
        'token': TOKEN,
        'channels': CHANNEL,
        'filename': str(jpg_num + 1) + '枚目'
    }
    requests.post(
        url="https://slack.com/api/files.upload",
        params=param,
        files=files)
