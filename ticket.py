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
            bet_price,
            expected_value,
            odds):
        self.opdt = opdt
        self.rcoursecd = rcoursecd
        self.rno = int(rno)
        self.denomination = denomination
        self.method = method
        self.multi = multi
        self.number = number
        self.bet_price = bet_price
        self.expected_value = int(expected_value)
        self.odds = odds

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
                self.number,
                int(self.bet_price),
                int(self.expected_value),
                self.odds]

    def to_verification_format(self):
        return 'Ticket=[opdt={}, rcoursecd={}, rno={}, denomination={}, number={}, bet_price={}, expected_value={}]'.format(
            self.opdt, self.rcoursecd, self.rno, self.denomination, self.number, self.bet_price, self.expected_value)

    def to_twitter_format(self):
        return convert_to_kanji(str(self.denomination)) + ' ' +  \
            str(self.number) + ' ' + str(self.bet_price) + '円'


def make_ticket(entry, realtime_odds):
    ticlet_list = []
    axis_list = []
    braid_list = []

    # 単勝購入
    realtime_tan_odds_list = realtime_odds.tan_odds_list
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, realtime_tan_odds_list))[0]

        bet = 0
        expected_value = horse.probability * odds.tanodds
        if expected_value >= 200 and odds.tanodds <= 30 and odds.tanodds >= 3.0:
            bet = lowest_bet_for(expected_value * 60, odds.tanodds)
        else:
            continue

        ticket = Ticket(
            entry.opdt,
            entry.rcoursecd,
            entry.rno,
            'TANSYO',
            'NORMAL',
            '',
            horse.umano,
            str(bet),
            expected_value,
            odds.tanodds)
        ticlet_list.append(ticket)

    # 複勝購入
    fuku_min_odds_list = realtime_odds.fuku_min_odds_list
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, fuku_min_odds_list))[0]

        fuku_probability = get_fuku_probability(horse.probability, entry)

        bet = 0
        expected_value = fuku_probability * odds.fuku_min_odds
        if expected_value >= 120 and odds.fuku_min_odds <= 7.0 and odds.fuku_min_odds >= 1.5:
            bet = lowest_bet_for(expected_value * 50, odds.fuku_min_odds)
        else:
            continue

        ticket_fuku = Ticket(
            entry.opdt,
            entry.rcoursecd,
            entry.rno,
            'FUKUSYO',
            'NORMAL',
            '',
            horse.umano,
            str(bet),
            expected_value,
            odds.fuku_min_odds)
        ticlet_list.append(ticket_fuku)

    realtime_wide_odds_list = realtime_odds.wide_odds_list

    # ワイドを購入
    for i, horse1 in enumerate(entry.horse_list):
        for horse2 in entry.horse_list[i + 1:]:
            pair_num = make_wide(horse1.umano, horse2.umano)
            odds = list(
                filter(
                    lambda real_odds: True if pair_num == real_odds.pair_umano else False,
                    realtime_wide_odds_list))[0]

            horse1_in_wide_probability = get_wide_probability(
                horse1.probability)
            horse2_in_wide_probability = get_wide_probability(
                horse2.probability)

            expected_value = odds.wideodds * horse1_in_wide_probability * \
                horse2_in_wide_probability / 100

            bet = 0
            if expected_value >= 500 and odds.wideodds <= 300 and odds.wideodds >= 30:
                bet = lowest_bet_for(expected_value * 10, odds.wideodds)
            else:
                continue

            ticket_wide = Ticket(
                entry.opdt,
                entry.rcoursecd,
                entry.rno,
                'WIDE',
                'NORMAL',
                '',
                make_wide(
                    horse1.umano,
                    horse2.umano),
                str(bet),
                expected_value,
                odds.wideodds)
            ticlet_list.append(ticket_wide)

    return ticlet_list


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


# 単勝率から複勝率を算出
def get_fuku_probability(x, entry):
    res = 5.8962 * \
        x ** 0.7112 if len(entry.horse_list) > 7 else get_ren_probability(x)  # 出走頭数に応じて
    return res if res < 95 else 95


# 単勝率から連対率を算出
def get_ren_probability(x):
    res = 3.5097 * x ** 0.794
    return res if res < 90 else 90


# 単勝率からワイド率を算出
def get_wide_probability(x):
    res = 5.8962 * x ** 0.7112
    return res if res < 95 else 95


def convert_to_kanji(txt):
    if 'TANSYO' in txt:
        return '単勝'
    if 'FUKUSYO' in txt:
        return '複勝'
    if 'WIDE' in txt:
        return 'ワイド'
