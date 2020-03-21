import time
import fdb
import pandas as pd


def make_connect():
    conn = fdb.connect(
        dsn='****',
        port=0000,
        user='****',
        password='****',
        charset='SJIS_0208'
    )
    return conn


def get_data(sql):
    start = time.time()

    conn = make_connect()
    df = pd.read_sql_query(sql=sql, con=conn)
    conn.close()

    elapsed_time = time.time() - start
    print("elapsed_time : {:.1f}".format(elapsed_time) + " [sec]")

    return df
