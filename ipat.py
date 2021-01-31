import os
import time

from dotenv import load_dotenv
from selenium import webdriver

# 環境変数の読み取り
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

INET_ID = os.environ.get('INET_ID')
ENTRY_NUM = os.environ.get('ENTRY_NUM')
SECRET_NUM = os.environ.get('SECRET_NUM')
P_ARS_NUM = os.environ.get('P_ARS_NUM')


def get_result_capture():
    # オプション追加
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--start-maximized')
    driver = get_webdriver(options)

    # ログインページを開く
    driver.get('https://www.ipat.jra.go.jp/')

    # ログイン情報を入力
    driver.find_element_by_name('inetid').send_keys(INET_ID)
    driver.find_element_by_class_name('button').click()
    time.sleep(2)

    # 加入者番号など入力
    driver.find_elements_by_class_name('type')[0].find_element_by_tag_name('input').send_keys(ENTRY_NUM)
    driver.find_elements_by_class_name('type')[1].find_element_by_tag_name('input').send_keys(SECRET_NUM)
    driver.find_elements_by_class_name('type')[2].find_element_by_tag_name('input').send_keys(P_ARS_NUM)
    driver.find_element_by_class_name('buttonModern').click()
    time.sleep(2)

    # 投票履歴をクリック
    driver.find_element_by_class_name('btn-reference').click()
    time.sleep(2)

    # # 倍率を変更
    # driver.execute_script("document.body.style.zoom='90%'")
    # time.sleep(2)
    #
    # # スクリーンショットを取る
    # w = driver.execute_script('return document.body.scrollWidth')
    # h = driver.execute_script('return document.body.scrollHeight')
    # driver.set_window_size(w, h)
    # driver.save_screenshot('./image/result.png')

    png = driver.find_element_by_class_name('balance-col').screenshot_as_png
    with open('./image/result.png', 'wb') as f:
        f.write(png)

    driver.quit()


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
