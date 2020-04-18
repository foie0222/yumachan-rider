import math


class Ticket:
    def __init__(
            self,
            opdt,
            rcoursecd,
            rno,
            denomination,
            method,
            multi,
            number,
            bet_price):
        self.opdt = opdt
        self.rcoursecd = rcoursecd
        self.rno = int(rno)
        self.denomination = denomination
        self.method = method
        self.multi = multi
        self.number = number
        self.bet_price = bet_price

    def to_string(self):
        return 'Ticket=[opdt={}, rcoursecd={}, rno={}, denomination={}, method={}, multi={}, number={}, bet_price={}]'.format(
            self.opdt, self.rcoursecd, self.rno, self.denomination, self.method, self.multi, self.number, self.bet_price)

    def to_csv(self):
        return '{},{},{},{},{},{},{},{}'.format(
            self.opdt,
            self.rcoursecd,
            self.rno,
            self.denomination,
            self.method,
            self.multi,
            self.number,
            self.bet_price)

    def to_gss_format(self):
        return [self.opdt,
                self.rcoursecd,
                self.rno,
                self.denomination,
                self.method,
                self.number,
                int(self.bet_price)]


def make_ticket(entry, realtime_odds):
    ticlet_list = []
    axis_list = []
    braid_list = []

    # 単勝購入
    realtime_tan_odds_list = realtime_odds.tan_odds_list
    for horse in entry.horse_list[:5]:
        # 軸馬一覧に追加
        axis_list.append(horse)

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, realtime_tan_odds_list))[0]

        bet = 0
        expected_value = horse.probability * odds.tanodds
        if expected_value >= 120:  # 単勝回収率が120%以上なら期待値に応じてベット
            bet = lowest_bet_for(expected_value * 15, odds.tanodds)

        if bet == 0:
            continue
        ticket = Ticket(entry.opdt, entry.rcoursecd, entry.rno,
                        'TANSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket)

    # 複勝購入
    fuku_min_odds_list = realtime_odds.fuku_min_odds_list
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, fuku_min_odds_list))[0]

        fuku_probability = get_fuku_probability(horse.probability)

        bet = 0
        if fuku_probability * odds.fuku_min_odds >= 120:  # 複勝回収率が120%以上なら払い戻しが3500円超える最低金額をベット
            bet = lowest_bet_for(4000, odds.fuku_min_odds)

        if bet >= 100 or horse.sign == 'braid':
            bet += 100

        if bet == 0:
            continue

        ticket_fuku = Ticket(entry.opdt, entry.rcoursecd, entry.rno,
                             'FUKUSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket_fuku)
        braid_list.append(horse)

    realtime_wide_odds_list = realtime_odds.wide_odds_list

    # ワイドを購入
    for axis in axis_list:
        for braid in braid_list:
            if axis.umano == braid.umano:
                continue

            pair_num = make_wide(axis.umano, braid.umano)
            odds = list(
                filter(
                    lambda real_odds: True if pair_num == real_odds.pair_umano else False,
                    realtime_wide_odds_list))[0]

            axis_in_wide_probability = get_fuku_probability(axis.probability)
            braid_in_wide_probability = get_fuku_probability(braid.probability)

            if odds.wideodds * axis_in_wide_probability * \
                    braid_in_wide_probability / 100 < 300:
                continue

            bet = lowest_bet_for(3500, odds.wideodds)

            ticket_wide = Ticket(
                entry.opdt,
                entry.rcoursecd,
                entry.rno,
                'WIDE',
                'NORMAL',
                '',
                make_wide(
                    axis.umano,
                    braid.umano),
                str(bet))
            ticlet_list.append(ticket_wide)

    return ticlet_list


def is_in_list(umano, axis_list):
    for axis in axis_list:
        if umano == axis.umano:
            return True
    return False


def lowest_bet_for(pay, odds):
    bet = 100
    while pay > odds * bet:
        bet += 100
    return bet


def make_wide(umano1, umano2):
    uma1 = int(umano1)
    uma2 = int(umano2)
    if uma1 < uma2:
        return umano1 + '-' + umano2
    return umano2 + '-' + umano1


# 軸馬と1番高確率の馬のリスト
def get_axis_list(horse_list):
    axis_list = [horse_list[0]]

    for horse in horse_list:
        if horse.sign == 'axis':
            axis_list.append(horse)

    return axis_list


# 単勝率から複勝率を算出
def get_fuku_probability(tan_probability):
    res = -0.00001 * tan_probability ** 4 + 0.0021 * tan_probability ** 3 - \
        0.1344 * tan_probability ** 2 + 4.4261 * tan_probability + 0.8811
    return res if res < 100 else 100


if __name__ == '__main__':
    print(get_fuku_probability(1.7))
