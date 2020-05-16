import dbconnector as con
import datetime
import shutil
import codecs


def make_task_xml():
    date = datetime.datetime.now()
    datetime_start_shcedule_list = get_schedule_list(date)
    bef2min_start_shcedule_list = rollback_2min(datetime_start_shcedule_list)
    xml_txt = make_xml_txt(bef2min_start_shcedule_list)
    make_target_xml()
    set_schedule(xml_txt)


def rollback_2min(datetime_start_shcedule_list):
    bef2min_start_shcedule_list = []
    for datetime_start_shcedule in datetime_start_shcedule_list:
        bef2min_start_shcedule = datetime_start_shcedule - \
            datetime.timedelta(minutes=2)  # 発走時刻の2分前
        bef2min_start_shcedule_list.append(bef2min_start_shcedule)
    return bef2min_start_shcedule_list


def get_schedule_list(date):
    opdt = get_opdt(date)  # like 20200516
    df_start_shcedule_list = con.get_data(
        """
        select
            POSTTM
        from
            RACEMST
        where
            OPDT = '{}'
        order by POSTTM
        """.format(opdt)
    )
    return convert_schedule_list(df_start_shcedule_list, date)


def convert_schedule_list(df_start_shcedule_list, date):
    start_shcedule_list = df_start_shcedule_list['POSTTM'].values.tolist()

    datetime_start_shcedule_list = []
    for start_shcedule in start_shcedule_list:
        start_time = get_start_time(start_shcedule, date)
        datetime_start_time = datetime.datetime.strptime(
            start_time, '%Y-%m-%d %H:%M:%S')
        datetime_start_shcedule_list.append(datetime_start_time)
    return datetime_start_shcedule_list


def get_start_time(start_shcedule, date):  # like '2020-05-16 15:00:00'
    return str(date.year) + '-' + str(date.month) + '-' + str(date.day) + \
        ' ' + start_shcedule[0:2] + ':' + start_shcedule[2:4] + ':00'


def get_opdt(date):
    return str(date.year).zfill(4) + str(date.month).zfill(2) + \
        str(date.day).zfill(2)


def make_xml_txt(bef2min_start_shcedule_list):
    res = ''
    for bef2min_start_shcedule in bef2min_start_shcedule_list:
        txt = '''
    <TimeTrigger>
      <StartBoundary>{}</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>'''.format(str(bef2min_start_shcedule).replace(' ', 'T'))
        res = res + txt
    return res


def make_target_xml():
    src = './xml/template.xml'
    copy = './xml/中央競馬投票.xml'
    shutil.copyfile(src, copy)


def set_schedule(xml_txt):
    filename = './xml/中央競馬投票.xml'
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        fileText = f.read()
        fileText = fileText.replace('target', xml_txt)

    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(fileText)


if __name__ == '__main__':
    make_task_xml()
