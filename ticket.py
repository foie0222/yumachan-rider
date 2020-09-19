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
        return 'Ticket=[opdt={}, rcoursecd={}, rno={}, denomination={}, number={}, bet_price={}, expected_value={}, odds={}]'.format(
            self.opdt, self.rcoursecd, self.rno, self.denomination, self.number, self.bet_price, self.expected_value, self.odds)

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
        if expected_value >= 150 and odds.tanodds <= 150 and odds.tanodds >= 5.0:
            bet = lowest_bet_for(expected_value * 330, odds.tanodds)
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
        if expected_value >= 110 and odds.fuku_min_odds <= 10.0 and odds.fuku_min_odds >= 3.0:
            bet = lowest_bet_for(expected_value * 500, odds.fuku_min_odds)
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

    # 馬連を購入
    just_before_umaren_odds_list = realtime_odds.umaren_odds_list
    umaren_ticket_list = []
    for i, horse1 in enumerate(entry.horse_list):
        for horse2 in entry.horse_list[i + 1:]:
            pair_num = make_wide(horse1.umano, horse2.umano)
            odds = list(
                filter(
                    lambda real_odds: True if pair_num == real_odds.pair_umano else False,
                    just_before_umaren_odds_list))[0]

            horse1_in_umaren_probability = get_ren_probability(
                horse1.probability)
            horse2_in_umaren_probability = get_ren_probability(
                horse2.probability)

            bet = 0
            expected_value = odds.umaren_odds * (
                horse1.probability * (
                    horse2_in_umaren_probability - horse2.probability) + horse2.probability * (
                    horse1_in_umaren_probability - horse1.probability)) / 100

            if expected_value >= 180 and odds.umaren_odds <= 800 and odds.umaren_odds >= 0:
                bet = lowest_bet_for(expected_value * 280, odds.umaren_odds)
            else:
                continue

            ticket_umaren = Ticket(
                entry.opdt,
                entry.rcoursecd,
                entry.rno,
                'UMAREN',
                'NORMAL',
                '',
                make_wide(
                    horse1.umano,
                    horse2.umano),
                str(bet),
                expected_value,
                odds.umaren_odds)
            umaren_ticket_list.append(ticket_umaren)

    sorted_umaren_ticket_list = sorted(
        umaren_ticket_list, key=lambda t: t.number)
    ticket_list.extend(sorted_umaren_ticket_list)

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
                bet = lowest_bet_for(expected_value * 170, odds.wideodds)
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

                bet = 0
                expected_value = get_trio_expected_possibility(
                    horse1.probability, horse2.probability, horse3.probability) * odds.trio_odds

                if expected_value >= 200 and odds.trio_odds <= 2000 and odds.trio_odds >= 0:
                    bet = lowest_bet_for(
                        expected_value * 250,
                        odds.trio_odds)
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


def make_verification_ticket(entry, just_before_odds):
    return make_ticket(entry, just_before_odds)

    # # 単勝購入
    # realtime_tan_odds_list = just_before_odds.tan_odds_list
    # tan_ticket_list = []
    # for horse in entry.horse_list:

    #     odds = list(filter(lambda real_odds: True if real_odds.umano ==
    # horse.umano else False, realtime_tan_odds_list))[0]

    #     bet = 0
    #     expected_value = horse.probability * odds.tanodds

    #     ticket = Ticket(
    #         entry.opdt,
    #         entry.rcoursecd,
    #         entry.rno,
    #         'TANSYO',
    #         'NORMAL',
    #         '',
    #         horse.umano,
    #         str(bet),
    #         expected_value,
    #         odds.tanodds)
    #     tan_ticket_list.append(ticket)

    # sorted_tan_ticket_list = sorted(tan_ticket_list, key=lambda t: t.number)
    # ticket_list.extend(sorted_tan_ticket_list)

    # # 複勝購入
    # fuku_min_odds_list = just_before_odds.fuku_min_odds_list
    # fuku_ticket_list = []
    # for horse in entry.horse_list:

    #     odds = list(filter(lambda real_odds: True if real_odds.umano ==
    #                        horse.umano else False, fuku_min_odds_list))[0]

    #     fuku_probability = get_fuku_probability(horse.probability, entry)

    #     bet = 0
    #     expected_value = fuku_probability * odds.fuku_min_odds

    #     ticket_fuku = Ticket(
    #         entry.opdt,
    #         entry.rcoursecd,
    #         entry.rno,
    #         'FUKUSYO',
    #         'NORMAL',
    #         '',
    #         horse.umano,
    #         str(bet),
    #         expected_value,
    #         odds.fuku_min_odds)
    #     fuku_ticket_list.append(ticket_fuku)

    # sorted_fuku_ticket_list = sorted(fuku_ticket_list, key=lambda t: t.number)
    # ticket_list.extend(sorted_fuku_ticket_list)

    # # 馬連を購入
    # just_before_umaren_odds_list = just_before_odds.umaren_odds_list
    # umaren_ticket_list = []
    # for i, horse1 in enumerate(entry.horse_list):
    #     for horse2 in entry.horse_list[i + 1:]:
    #         pair_num = make_wide(horse1.umano, horse2.umano)
    #         odds = list(
    #             filter(
    #                 lambda real_odds: True if pair_num == real_odds.pair_umano else False,
    #                 just_before_umaren_odds_list))[0]

    #         horse1_in_umaren_probability = get_ren_probability(
    #             horse1.probability)
    #         horse2_in_umaren_probability = get_ren_probability(
    #             horse2.probability)

    #         expected_value = odds.umaren_odds * (
    #             horse1.probability * (
    #                 horse2_in_umaren_probability - horse2.probability) + horse2.probability * (
    #                 horse1_in_umaren_probability - horse1.probability)) / 100

    #         bet = 0

    #         ticket_umaren = Ticket(
    #             entry.opdt,
    #             entry.rcoursecd,
    #             entry.rno,
    #             'UMAREN',
    #             'NORMAL',
    #             '',
    #             make_wide(
    #                 horse1.umano,
    #                 horse2.umano),
    #             str(bet),
    #             expected_value,
    #             odds.umaren_odds)
    #         umaren_ticket_list.append(ticket_umaren)

    # sorted_umaren_ticket_list = sorted(
    #     umaren_ticket_list, key=lambda t: t.number)
    # ticket_list.extend(sorted_umaren_ticket_list)

    # # ワイドを購入
    # realtime_wide_odds_list = just_before_odds.wide_odds_list
    # wide_ticket_list = []
    # for i, horse1 in enumerate(entry.horse_list):
    #     for horse2 in entry.horse_list[i + 1:]:
    #         pair_num = make_wide(horse1.umano, horse2.umano)
    #         odds = list(
    #             filter(
    #                 lambda real_odds: True if pair_num == real_odds.pair_umano else False,
    #                 realtime_wide_odds_list))[0]

    #         horse1_in_wide_probability = get_wide_probability(
    #             horse1.probability)
    #         horse2_in_wide_probability = get_wide_probability(
    #             horse2.probability)

    #         expected_value = odds.wideodds * horse1_in_wide_probability * \
    #             horse2_in_wide_probability / 100

    #         bet = 0
    #         if expected_value >= 300 and odds.wideodds <= 150 and odds.wideodds >= 20:
    #             bet = lowest_bet_for(expected_value * 80, odds.wideodds)
    #         else:
    #             continue

    #         ticket_wide = Ticket(
    #             entry.opdt,
    #             entry.rcoursecd,
    #             entry.rno,
    #             'WIDE',
    #             'NORMAL',
    #             '',
    #             make_wide(
    #                 horse1.umano,
    #                 horse2.umano),
    #             str(bet),
    #             expected_value,
    #             odds.wideodds)
    #         wide_ticket_list.append(ticket_wide)

    # sorted_wide_ticket_list = sorted(wide_ticket_list, key=lambda t: t.number)
    # ticket_list.extend(sorted_wide_ticket_list)

    # # 3連複を購入
    # realtime_trio_odds_list = just_before_odds.trio_odds_list
    # trio_ticket_list = []
    # for index1, horse1 in enumerate(entry.horse_list):
    #     for index2, horse2 in enumerate(entry.horse_list[index1 + 1:]):
    #         for horse3 in entry.horse_list[index1 + index2 + 2:]:
    #             pair_num = make_trio(horse1.umano, horse2.umano, horse3.umano)

    #             odds = list(
    #                 filter(
    #                     lambda real_odds: True if pair_num == real_odds.pair_umano else False,
    #                     realtime_trio_odds_list))[0]

    #             bet = 0
    #             expected_value = get_trio_expected_possibility(
    # horse1.probability, horse2.probability, horse3.probability) *
    # odds.trio_odds

    #             ticket_trio = Ticket(
    #                 entry.opdt,
    #                 entry.rcoursecd,
    #                 entry.rno,
    #                 'SANRENPUKU',
    #                 'NORMAL',
    #                 '',
    #                 make_trio(
    #                     horse1.umano,
    #                     horse2.umano,
    #                     horse3.umano),
    #                 str(bet),
    #                 expected_value,
    #                 odds.trio_odds)
    #             trio_ticket_list.append(ticket_trio)

    # sorted_trio_ticket_list = sorted(trio_ticket_list, key=lambda t: t.number)
    # ticket_list.extend(sorted_trio_ticket_list)

    # return ticket_list


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


# 単勝率から3連複率を算出
def get_trio_expected_possibility(x, y, z):
    x_y_z = x * (get_ren_probability(y) - y) * \
        (get_wide_probability(z) - get_ren_probability(z)) / 1000000
    x_z_y = x * (get_ren_probability(z) - z) * \
        (get_wide_probability(y) - get_ren_probability(y)) / 1000000
    y_x_z = y * (get_ren_probability(x) - x) * \
        (get_wide_probability(z) - get_ren_probability(z)) / 1000000
    y_z_x = y * (get_ren_probability(z) - z) * \
        (get_wide_probability(x) - get_ren_probability(x)) / 1000000
    z_x_y = z * (get_ren_probability(x) - x) * \
        (get_wide_probability(y) - get_ren_probability(y)) / 1000000
    z_y_x = z * (get_ren_probability(y) - y) * \
        (get_wide_probability(x) - get_ren_probability(x)) / 1000000

    possibility = x_y_z + x_z_y + y_x_z + y_z_x + z_x_y + z_y_x
    return possibility * 100


def convert_to_kanji(txt):
    if 'TANSYO' in txt:
        return '単勝'
    if 'FUKUSYO' in txt:
        return '複勝'
    if 'UMAREN' in txt:
        return '馬連'
    if 'WIDE' in txt:
        return 'ワイド'
    if 'SANRENPUKU' in txt:
        return '3連複'
