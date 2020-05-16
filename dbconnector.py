import time
import fdb
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数の読み取り
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def make_connect():
    conn = fdb.connect(
        dsn=os.environ.get('DSN'),
        port=os.environ.get('PORT'),
        user=os.environ.get('DBUSER'),
        password=os.environ.get('PASSWORD'),
        charset='SJIS_0208'
    )
    return conn


def get_data(sql):
    start = time.time()

    conn = make_connect()
    df = pd.read_sql_query(sql=sql, con=conn)
    conn.close()

    elapsed_time = time.time() - start

    return df
