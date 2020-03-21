import dbconnector as con


class Odds:
    def __init__(self, umano, tanodds):
        self.umano = umano
        self.tanodds = tanodds

    def to_string(self):
        return 'Odds=[umano={}, tanodds={}]'.format(self.umano, self.tanodds)


def get_realtime_odds(opdt, rcoursecd, rno):
    rcourse = convert_rcoursecd_num(rcoursecd)
    realtime_odds = con.get_data(
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
    return convert_odds_list(realtime_odds)


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


def convert_odds_list(realtime_odds):
    odds_row = str(realtime_odds['TANODDS'][0])
    odds_value_list = [odds_row[i: i + 4] for i in range(0, len(odds_row), 4)] #4桁ずつ分割

    odds_list = []
    for index, odds_value in enumerate(odds_value_list):
        odds_list.append(Odds(get_num_from_index(index), convert_float(odds_value)))

    return odds_list


def convert_float(odds_value):
    return float(odds_value) / 10


def get_num_from_index(index):
    return str(index + 1).zfill(2)


# if __name__ == '__main__':
#     get_realtime_odds('20200320', '06', '04')

