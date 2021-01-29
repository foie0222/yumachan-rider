import os
import gspread
import time
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# 環境変数の読み取り
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

SPREADSHEET_KEY = os.environ.get('SPREADSHEET_KEY')


def write_gss(record_list, timestamp, is_main):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # 認証情報
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credential/keibaautovote.json', scope)
    gc = gspread.authorize(credentials)

    # 対象のスプレッドシートを取得
    spreadsheet = gc.open_by_key(SPREADSHEET_KEY)

    # ワークシート一覧にシートがあるかチェックしてなければ作成する
    worksheets = spreadsheet.worksheets()
    sheet_name = timestamp[:8]
    if not existSheet(worksheets, sheet_name):
        spreadsheet.add_worksheet(title=sheet_name, rows=300, cols=26)

    # 対象のシートを指定（日付ごと）
    worksheet = spreadsheet.worksheet(sheet_name)

    # 購入リストを1件ずつスプレッドシートに書き出す
    for record in record_list:
        worksheet.append_row(record.to_gss_format())
        time.sleep(1)


# シートの存在チェック
def existSheet(worksheets, sheet_name):
    for sheet in worksheets:
        if sheet_name == sheet.title:
            return True
    return False
