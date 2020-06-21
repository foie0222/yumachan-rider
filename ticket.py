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
    ticket_list = []

    # 単勝購入
    realtime_tan_odds_list = realtime_odds.tan_odds_list
    tan_ticket_list = []
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, realtime_tan_odds_list))[0]

        bet = 0
        expected_value = horse.probability * odds.tanodds
        if expected_value >= 180 and odds.tanodds <= 300 and odds.tanodds >= 3.0:
            bet = lowest_bet_for(expected_value * 70, odds.tanodds)
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
        tan_ticket_list.append(ticket)

    sorted_tan_ticket_list = sorted(tan_ticket_list, key=lambda t: t.number)
    ticket_list.extend(sorted_tan_ticket_list)

    # 複勝購入
    fuku_min_odds_list = realtime_odds.fuku_min_odds_list
    fuku_ticket_list = []
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano ==
                           horse.umano else False, fuku_min_odds_list))[0]

        fuku_probability = get_fuku_probability(horse.probability, entry)

        bet = 0
        expected_value = fuku_probability * odds.fuku_min_odds
        if expected_value >= 120 and odds.fuku_min_odds <= 7.0 and odds.fuku_min_odds >= 1.5:
            bet = lowest_bet_for(expected_value * 80, odds.fuku_min_odds)
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
        fuku_ticket_list.append(ticket_fuku)

    sorted_fuku_ticket_list = sorted(fuku_ticket_list, key=lambda t: t.number)
    ticket_list.extend(sorted_fuku_ticket_list)

    # ワイドを購入
    realtime_wide_odds_list = realtime_odds.wide_odds_list
    wide_ticket_list = []
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
            if expected_value >= 300 and odds.wideodds <= 150 and odds.wideodds >= 20:
                bet = lowest_bet_for(expected_value * 60, odds.wideodds)
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
            wide_ticket_list.append(ticket_wide)

    sorted_wide_ticket_list = sorted(wide_ticket_list, key=lambda t: t.number)
    ticket_list.extend(sorted_wide_ticket_list)

    # 3連複を購入
    realtime_trio_odds_list = realtime_odds.trio_odds_list
    trio_ticket_list = []
    for index1, horse1 in enumerate(entry.horse_list):
        for index2, horse2 in enumerate(entry.horse_list[index1 + 1:]):
            for horse3 in entry.horse_list[index1 + index2 + 2:]:
                pair_num = make_trio(horse1.umano, horse2.umano, horse3.umano)

                odds = list(
                    filter(
                        lambda real_odds: True if pair_num == real_odds.pair_umano else False,
                        realtime_trio_odds_list))[0]

                horse1_in_trio_probability = get_wide_probability(
                    horse1.probability)
                horse2_in_trio_probability = get_wide_probability(
                    horse2.probability)
                horse3_in_trio_probability = get_wide_probability(
                    horse3.probability)

                bet = 0
                expected_trio_final_odds = odds.trio_odds * 0.9
                expected_value = expected_trio_final_odds * horse1_in_trio_probability * \
                    horse2_in_trio_probability * horse3_in_trio_probability / 10000
                if expected_value >= 1000 and expected_trio_final_odds <= 2000 and expected_trio_final_odds >= 100:
                    bet = lowest_bet_for(
                        expected_value * 10,
                        expected_trio_final_odds)
                else:
                    continue

                ticket_trio = Ticket(
                    entry.opdt,
                    entry.rcoursecd,
                    entry.rno,
                    'SANRENPUKU',
                    'NORMAL',
                    '',
                    make_trio(
                        horse1.umano,
                        horse2.umano,
                        horse3.umano),
                    str(bet),
                    expected_value,
                    odds.trio_odds)
                trio_ticket_list.append(ticket_trio)

    sorted_trio_ticket_list = sorted(trio_ticket_list, key=lambda t: t.number)
    ticket_list.extend(sorted_trio_ticket_list)

    return ticket_list


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


def make_trio(umano1, umano2, umano3):
    x = [int(umano1), int(umano2), int(umano3)]
    sorted_x = sorted(x)
    res = str(sorted_x[0]).zfill(2) + '-' + \
        str(sorted_x[1]).zfill(2) + '-' + str(sorted_x[2]).zfill(2)
    return res


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
    if 'SANRENPUKU' in txt:
        return '3連複'
