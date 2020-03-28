import dbconnector as con


class Odds:
    def __init__(self, tan_odds_list, wide_odds_list):
        self.tan_odds_list = tan_odds_list
        self.wide_odds_list = wide_odds_list


class TanOdds:
    def __init__(self, umano, tanodds):
        self.umano = umano
        self.tanodds = tanodds

    def to_string(self):
        return 'TanOdds=[umano={}, tanodds={}]'.format(self.umano, self.tanodds)


class WideOdds:
    def __init__(self, pair_umano, wideodds):
        self.pair_umano = pair_umano  # like 01-03
        self.wideodds = wideodds

    def to_string(self):
        return 'WideOdds=[pair_umano={}, wideodds={}]'.format(self.pair_umano, self.wideodds)


def get_realtime_odds(opdt, rcoursecd, rno):
    return Odds(get_realtime_tan_odds(opdt, rcoursecd, rno), get_realtime_wide_odds(opdt, rcoursecd, rno))


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


def convert_tan_odds_list(realtime_tan_odds):
    tan_odds_row = str(realtime_tan_odds['TANODDS'][0])
    tan_odds_value_list = [tan_odds_row[i: i + 4] for i in range(0, len(tan_odds_row), 4)]  # 4桁ずつ分割

    tan_odds_list = []
    for index, odds_value in enumerate(tan_odds_value_list):
        tan_odds_list.append(TanOdds(get_num_from_index(index), convert_float(odds_value)))

    return tan_odds_list


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
        wide_odds_value_list = [wide_odds_row[i: i + 5] for i in range(0, len(wide_odds_row), 5)]  # 5桁ずつ分割

        for index, odds_value in enumerate(wide_odds_value_list):
            if odds_value == 'None':
                continue
            wide_odds_list.append(WideOdds(get_pair_num_from_column_and_index(column, index), convert_float(odds_value)))

    return wide_odds_list


# 馬の連番を抽出
def get_pair_num_from_column_and_index(column, index):
    umano_column = column.replace('WIDEMINODDS', '')
    return umano_column + '-' + str(int(umano_column) + index + 1).zfill(2)


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
    if odds_value == '****' or odds_value == '*****':
        return 0
    return float(odds_value) / 10


def get_num_from_index(index):
    return str(index + 1).zfill(2)


if __name__ == '__main__':
    get_realtime_wide_odds('20200322', 'HANSHIN', '12')
