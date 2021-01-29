import json
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

# 環境変数の読み取り
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

CK = os.environ.get('TWITTER_API_KEY')
CS = os.environ.get('TWITTER_API_KEY_SECRET')
AT = os.environ.get('TWITTER_ACCESS_TOKEN')
AS = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')


def tweet(path_list_images):
    oauth = OAuth1Session(CK, CS, AT, AS)

    url_media = 'https://upload.twitter.com/1.1/media/upload.json'
    url_text = 'https://api.twitter.com/1.1/statuses/update.json'

    media_ids = ''

    # 画像の枚数分ループ
    for path in path_list_images:
        files = {'media': open(path, 'rb')}
        req_media = oauth.post(url_media, files=files)

        # レスポンスを確認
        if req_media.status_code != 200:
            print('画像アップデート失敗: {}'.format(req_media.text))
            return -1

        media_id = json.loads(req_media.text)['media_id']
        media_id_string = json.loads(req_media.text)['media_id_string']
        print('Media ID: {} '.format(media_id))
        # メディアIDの文字列をカンマ','で結合
        if media_ids == '':
            media_ids += media_id_string
        else:
            media_ids = media_ids + ',' + media_id_string

    print('media_ids: ', media_ids)
    params = {'status': '', 'media_ids': [media_ids]}
    req_text = oauth.post(url_text, params=params)

    # 再びレスポンスを確認
    if req_text.status_code != 200:
        print("テキストアップデート失敗: {}".format(req_text.text))
        return -1

    print("tweet uploaded\n")
    return 1


if __name__ == '__main__':
    tweet(['./image/vote.jpg'])
