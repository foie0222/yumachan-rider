import gspread
from oauth2client.service_account import ServiceAccountCredentials

SPREADSHEET_KEY = '1xjthz5vd-zuAqTI6FXrI_G6ldGIDiXXev4pgnFexJ4o'


def write_gss(ticket_list, timestamp):
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
        spreadsheet.add_worksheet(title=sheet_name, rows=150, cols=26)

    # 対象のシートを指定
    worksheet = spreadsheet.worksheet(sheet_name)

    # 購入リストを1件ずつスプレッドシートに書き出す
    for ticket in ticket_list:
        rowToAdd = [
            ticket.opdt,
            ticket.rcourcecd,
            ticket.rno,
            ticket.denomination,
            ticket.method,
            ticket.number,
            ticket.bet_price]
        worksheet.append_row(rowToAdd)


# シートの存在チェック
def existSheet(worksheets, sheet_name):
    for sheet in worksheets:
        if sheet_name == sheet.title:
            return True
    return False
