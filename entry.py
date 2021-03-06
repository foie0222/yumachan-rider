from horse import get_horse_list, get_horse_list_from_png_by_google
import re


class Entry:
    def __init__(self, opdt, rcoursecd, rno, rname, horse_list):
        self.opdt = opdt
        self.rcoursecd = rcoursecd
        self.rno = rno
        self.rname = rname
        self.horse_list = horse_list


def get_entry(header_txt, body_txt):
    opdt = get_opdt(header_txt)
    rcoursecd = get_rcoursecd(re.findall('.*R', header_txt)[0])
    rno = get_rno(header_txt)
    rname = get_rname(header_txt)
    horser_list = get_horse_list(body_txt)

    return Entry(opdt, rcoursecd, rno, rname, horser_list)


def get_entry_by_png(header_txt, png_url):
    opdt = get_opdt(header_txt)
    rcourse = get_rcoursecd(header_txt[:15])
    rno = get_rno(header_txt)
    rname = get_rname(header_txt)
    horser_list = get_horse_list_from_png_by_google(png_url)

    return Entry(opdt, rcourse, rno, rname, horser_list)


def get_opdt(row):
    return row[0:8]


def get_rcoursecd(row):
    if '札幌' in row:
        return 'SAPPORO'
    if '函館' in row:
        return 'HAKODATE'
    if '福島' in row:
        return 'FUKUSHIMA'
    if '新潟' in row:
        return 'NIIGATA'
    if '東京' in row:
        return 'TOKYO'
    if '中山' in row:
        return 'NAKAYAMA'
    if '中京' in row:
        return 'CHUKYO'
    if '京都' in row:
        return 'KYOTO'
    if '阪神' in row:
        return 'HANSHIN'
    if '小倉' in row:
        return 'KOKURA'
    return None


def get_rno(row):
    return row[11:].split('R')[0].zfill(2)


def get_rname(row):
    return row.split('R ')[1]
