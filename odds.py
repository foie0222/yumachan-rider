import dbconnector as con


class Odds:
    def __init__(
            self,
            tan_odds_list,
            fuku_min_odds_list,
            wide_odds_list,
            trio_odds_list):
        self.tan_odds_list = tan_odds_list
        self.fuku_min_odds_list = fuku_min_odds_list
        self.wide_odds_list = wide_odds_list
        self.trio_odds_list = trio_odds_list


class TanOdds:
    def __init__(self, umano, tanodds):
        self.umano = umano
        self.tanodds = tanodds

    def to_string(self):
        return 'TanOdds=[umano={}, tanodds={}]'.format(
            self.umano, self.tanodds)


class FukuMinOdds:
    def __init__(self, umano, fuku_min_odds):
        self.umano = umano
        self.fuku_min_odds = fuku_min_odds

    def to_string(self):
        return 'FukuMinOdds=[umano={}, fuku_min_odds={}]'.format(
            self.umano, self.fuku_min_odds)


class WideOdds:
    def __init__(self, pair_umano, wideodds):
        self.pair_umano = pair_umano  # like 01-03
        self.wideodds = wideodds

    def to_string(self):
        return 'WideOdds=[pair_umano={}, wideodds={}]'.format(
            self.pair_umano, self.wideodds)


class TrioOdds:
    def __init__(self, pair_umano, trio_odds):
        self.pair_umano = pair_umano  # like 01-03-04
        self.trio_odds = trio_odds

    def to_string(self):
        return 'Trioodds=[pair_umano={}, trio_odds={}]'.format(
            self.pair_umano, self.trio_odds)


def get_realtime_odds(opdt, rcoursecd, rno):
    return Odds(
        get_realtime_tan_odds(opdt, rcoursecd, rno),
        get_realtime_fuku_min_odds(opdt, rcoursecd, rno),
        get_realtime_wide_odds(opdt, rcoursecd, rno),
        get_realtime_trio_odds(opdt, rcoursecd, rno))


# 検証用に直前オッズを取得
def get_just_before_odds(opdt, rcoursecd, rno):
    return Odds(
        get_just_before_tan_odds(opdt, rcoursecd, rno),
        get_just_before_fuku_odds(opdt, rcoursecd, rno),
        get_realtime_wide_odds(opdt, rcoursecd, rno),  # ワイドは直前オッズを取得できない
        get_realtime_trio_odds(opdt, rcoursecd, rno))  # 3連複は直前オッズを取得できない


# リアルタイムオッズを取得
def get_realtime_tan_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    realtime_tan_odds = con.get_data(
        """
        select
            TANODDS
        from
            ODDSTFWK
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        """.format(opdt, rcourse, rno)
    )
    return convert_tan_odds_list(realtime_tan_odds)


# 検証用に直前オッズを取得
def get_just_before_tan_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    just_before_tan_odds = con.get_data(
        """
        select
            TANODDS
        from
            RODDSTFWK
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        and
            RLSDTTM < '{}' ||  (select POSTTM from RACEMST where OPDT = '{}' and rcoursecd = '{}' and rno = '{}')
        order by
            RLSDTTM desc
        rows 1
        """.format(opdt, rcourse, rno, opdt[4:8], opdt, rcourse, rno)
    )
    return convert_tan_odds_list(just_before_tan_odds)


def convert_tan_odds_list(realtime_tan_odds):
    tan_odds_row = str(realtime_tan_odds['TANODDS'][0])
    tan_odds_value_list = [tan_odds_row[i: i + 4]
                           for i in range(0, len(tan_odds_row), 4)]  # 4桁ずつ分割

    tan_odds_list = []
    for index, odds_value in enumerate(tan_odds_value_list):
        tan_odds_list.append(
            TanOdds(
                get_num_from_index(index),
                convert_float(odds_value)))

    return tan_odds_list


# リアルタイムオッズを取得
def get_realtime_fuku_min_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    realtime_fuku_min_odds = con.get_data(
        """
        select
            FUKMINODDS
        from
            ODDSTFWK
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        """.format(opdt, rcourse, rno)
    )
    return convert_fuku_min_odds_list(realtime_fuku_min_odds)


# 検証用に直前オッズを取得
def get_just_before_fuku_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    just_before_fuku_odds = con.get_data(
        """
        select
            FUKMINODDS
        from
            RODDSTFWK
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        and
            RLSDTTM < '{}' ||  (select POSTTM from RACEMST where OPDT = '{}' and rcoursecd = '{}' and rno = '{}')
        order by
            RLSDTTM desc
        rows 1
        """.format(opdt, rcourse, rno, opdt[4:8], opdt, rcourse, rno)
    )
    return convert_fuku_min_odds_list(just_before_fuku_odds)


def convert_fuku_min_odds_list(realtime_fuku_min_odds):
    fuku_min_odds_row = str(realtime_fuku_min_odds['FUKMINODDS'][0])
    fuku_min_odds_value_list = [fuku_min_odds_row[i: i + 4]
                                for i in range(0, len(fuku_min_odds_row), 4)]  # 4桁ずつ分割

    fuku_min_odds_list = []
    for index, fuku_min_odds_value in enumerate(fuku_min_odds_value_list):
        fuku_min_odds_list.append(
            FukuMinOdds(
                get_num_from_index(index),
                convert_float(fuku_min_odds_value)))

    return fuku_min_odds_list


def get_realtime_wide_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    realtime_wide_odds = con.get_data(
        """
        select
            WIDEMINODDS01,
            WIDEMINODDS02,
            WIDEMINODDS03,
            WIDEMINODDS04,
            WIDEMINODDS05,
            WIDEMINODDS06,
            WIDEMINODDS07,
            WIDEMINODDS08,
            WIDEMINODDS09,
            WIDEMINODDS10,
            WIDEMINODDS11,
            WIDEMINODDS12,
            WIDEMINODDS13,
            WIDEMINODDS14,
            WIDEMINODDS15,
            WIDEMINODDS16,
            WIDEMINODDS17
        from
            ODDSWIDE
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        """.format(opdt, rcourse, rno)
    )
    return convert_wide_odds_list(realtime_wide_odds)


def convert_wide_odds_list(realtime_wide_odds):
    wide_odds_list = []
    for column, row in realtime_wide_odds.iteritems():
        wide_odds_row = str(realtime_wide_odds[column][0])
        wide_odds_value_list = [wide_odds_row[i: i + 5]
                                for i in range(0, len(wide_odds_row), 5)]  # 5桁ずつ分割

        for index, odds_value in enumerate(wide_odds_value_list):
            if odds_value == 'None':
                continue
            wide_odds_list.append(
                WideOdds(
                    get_pair_num_from_column_and_index(
                        column,
                        index),
                    convert_float(odds_value)))

    return wide_odds_list


def get_realtime_trio_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    realtime_trio_odds = con.get_data(
        """
        select
            TRIOODDS0102,
            TRIOODDS0103,
            TRIOODDS0104,
            TRIOODDS0105,
            TRIOODDS0106,
            TRIOODDS0107,
            TRIOODDS0108,
            TRIOODDS0109,
            TRIOODDS0110,
            TRIOODDS0111,
            TRIOODDS0112,
            TRIOODDS0113,
            TRIOODDS0114,
            TRIOODDS0115,
            TRIOODDS0116,
            TRIOODDS0117,
            TRIOODDS0203,
            TRIOODDS0204,
            TRIOODDS0205,
            TRIOODDS0206,
            TRIOODDS0207,
            TRIOODDS0208,
            TRIOODDS0209,
            TRIOODDS0210,
            TRIOODDS0211,
            TRIOODDS0212,
            TRIOODDS0213,
            TRIOODDS0214,
            TRIOODDS0215,
            TRIOODDS0216,
            TRIOODDS0217,
            TRIOODDS0304,
            TRIOODDS0305,
            TRIOODDS0306,
            TRIOODDS0307,
            TRIOODDS0308,
            TRIOODDS0309,
            TRIOODDS0310,
            TRIOODDS0311,
            TRIOODDS0312,
            TRIOODDS0313,
            TRIOODDS0314,
            TRIOODDS0315,
            TRIOODDS0316,
            TRIOODDS0317,
            TRIOODDS0405,
            TRIOODDS0406,
            TRIOODDS0407,
            TRIOODDS0408,
            TRIOODDS0409,
            TRIOODDS0410,
            TRIOODDS0411,
            TRIOODDS0412,
            TRIOODDS0413,
            TRIOODDS0414,
            TRIOODDS0415,
            TRIOODDS0416,
            TRIOODDS0417,
            TRIOODDS0506,
            TRIOODDS0507,
            TRIOODDS0508,
            TRIOODDS0509,
            TRIOODDS0510,
            TRIOODDS0511,
            TRIOODDS0512,
            TRIOODDS0513,
            TRIOODDS0514,
            TRIOODDS0515,
            TRIOODDS0516,
            TRIOODDS0517,
            TRIOODDS0607,
            TRIOODDS0608,
            TRIOODDS0609,
            TRIOODDS0610,
            TRIOODDS0611,
            TRIOODDS0612,
            TRIOODDS0613,
            TRIOODDS0614,
            TRIOODDS0615,
            TRIOODDS0616,
            TRIOODDS0617,
            TRIOODDS0708,
            TRIOODDS0709,
            TRIOODDS0710,
            TRIOODDS0711,
            TRIOODDS0712,
            TRIOODDS0713,
            TRIOODDS0714,
            TRIOODDS0715,
            TRIOODDS0716,
            TRIOODDS0717,
            TRIOODDS0809,
            TRIOODDS0810,
            TRIOODDS0811,
            TRIOODDS0812,
            TRIOODDS0813,
            TRIOODDS0814,
            TRIOODDS0815,
            TRIOODDS0816,
            TRIOODDS0817,
            TRIOODDS0910,
            TRIOODDS0911,
            TRIOODDS0912,
            TRIOODDS0913,
            TRIOODDS0914,
            TRIOODDS0915,
            TRIOODDS0916,
            TRIOODDS0917,
            TRIOODDS1011,
            TRIOODDS1012,
            TRIOODDS1013,
            TRIOODDS1014,
            TRIOODDS1015,
            TRIOODDS1016,
            TRIOODDS1017,
            TRIOODDS1112,
            TRIOODDS1113,
            TRIOODDS1114,
            TRIOODDS1115,
            TRIOODDS1116,
            TRIOODDS1117,
            TRIOODDS1213,
            TRIOODDS1214,
            TRIOODDS1215,
            TRIOODDS1216,
            TRIOODDS1217,
            TRIOODDS1314,
            TRIOODDS1315,
            TRIOODDS1316,
            TRIOODDS1317,
            TRIOODDS1415,
            TRIOODDS1416,
            TRIOODDS1417,
            TRIOODDS1516,
            TRIOODDS1517,
            TRIOODDS1617
        from
            ODDSTRIO
        where
            OPDT = '{}'
        and
            rcoursecd = '{}'
        and
            rno = '{}'
        """.format(opdt, rcourse, rno)
    )
    return convert_trio_odds_list(realtime_trio_odds)


def convert_trio_odds_list(realtime_trio_odds):
    trio_odds_list = []
    for column, row in realtime_trio_odds.iteritems():
        trio_odds_row = str(realtime_trio_odds[column][0])
        trio_odds_value_list = [trio_odds_row[i: i + 6]
                                for i in range(0, len(trio_odds_row), 6)]  # 6桁ずつ分割

        for index, odds_value in enumerate(trio_odds_value_list):
            if odds_value == 'None':
                continue
            trio_odds_list.append(
                TrioOdds(
                    get_trio_pair_num(
                        column,
                        index),
                    convert_float(odds_value)))

    return trio_odds_list


# 馬の連番を抽出
def get_pair_num_from_column_and_index(column, index):
    umano_column = column.replace('WIDEMINODDS', '')
    return umano_column + '-' + str(int(umano_column) + index + 1).zfill(2)


# 馬の3連番を抽出
def get_trio_pair_num(column, index):
    umano_column = column.replace('TRIOODDS', '')
    umano1 = umano_column[0:2]
    umano2 = umano_column[2:4]
    return umano1 + '-' + umano2 + '-' + str(int(umano2) + index + 1).zfill(2)


def convert_rcoursecd_num(rcoursecd):
    if 'SAPPORO' in rcoursecd:
        return '01'
    if 'HAKODATE' in rcoursecd:
        return '02'
    if 'FUKUSHIMA' in rcoursecd:
        return '03'
    if 'NIIGATA' in rcoursecd:
        return '04'
    if 'TOKYO' in rcoursecd:
        return '05'
    if 'NAKAYAMA' in rcoursecd:
        return '06'
    if 'CHUKYO' in rcoursecd:
        return '07'
    if 'KYOTO' in rcoursecd:
        return '08'
    if 'HANSHIN' in rcoursecd:
        return '09'
    if 'KOKURA' in rcoursecd:
        return '10'
    return rcoursecd


def convert_float(odds_value):
    if '*' in odds_value or '-' in odds_value:
        return 0
    return float(odds_value) / 10


def get_num_from_index(index):
    return str(index + 1).zfill(2)
