class Ticket:
    def __init__(self, opdt, rcourcecd, rno, denomination, method, multi, number, bet_price):
        self.opdt = opdt
        self.rcourcecd = rcourcecd
        self.rno = int(rno)
        self.denomination = denomination
        self.method = method
        self.multi = multi
        self.number = number
        self.bet_price = bet_price

    def to_string(self):
        return 'Ticket=[opdt={}, rcourcecd={}, rno={}, denomination={}, method={}, multi={}, number={}, bet_price={}]'.format(
            self.opdt, self.rcourcecd, self.rno, self.denomination, self.method, self.multi, self.number, self.bet_price)

    def to_csv(self):
        return '{},{},{},{},{},{},{},{}'.format(self.opdt, self.rcourcecd, self.rno, self.denomination, self.method, self.multi,
                                                self.number, self.bet_price)


def make_ticket(entry, realtime_odds):
    ticlet_list = []
    axis_list = []
    braid_list = []

    realtime_tan_odds_list = realtime_odds.tan_odds_list

    # 軸馬の単勝馬券を購入
    for index, horse in enumerate(entry.horse_list[:4]):

        odds = list(filter(lambda real_odds: True if real_odds.umano == horse.umano else False, realtime_tan_odds_list))[0]

        bet = 0
        if horse.probability * odds.tanodds >= 135:  # 単勝回収率が135%以上なら払い戻しが3000円超える最低金額をベット
            bet = lowest_bet_for(3000, odds.tanodds)
        if horse.probability * odds.tanodds >= 145:  # 単勝回収率が145%以上なら払い戻しが5000円超える最低金額をベット
            bet = lowest_bet_for(5000, odds.tanodds)

        if bet > 0 or horse.sign == 'axis' or index == 0:  # 購入金額が100円以上もしくは軸の表記がある馬、最も高確率の馬は軸馬リストに追加
            axis_list.append(horse)

        if odds.tanodds < 5 or bet == 0:  # 単勝オッズが5倍以下なら購入見送り
            continue
        ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket)

    # 紐馬（紐のサインがある、もしくは単勝回収率170%以上）の単勝・複勝を購入
    for horse in entry.horse_list:

        odds = list(filter(lambda real_odds: True if real_odds.umano == horse.umano else False, realtime_tan_odds_list))[0]

        bet = 0
        if horse.probability * odds.tanodds >= 180:  # 単勝回収率が180%以上なら払い戻しが3000円超える最低金額をベット
            bet = lowest_bet_for(3000, odds.tanodds)

        if bet > 0 or horse.sign == 'braid':  # 購入金額が100円以上か紐の表記がある馬は紐馬リストに追加
            braid_list.append(horse)

        if odds.tanodds < 20 or bet == 0 or is_in_list(horse.umano, axis_list):  # 単勝オッズが20倍以下もしくは軸馬なら購入見送り
            continue
        ticket_tan = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket_tan)

    realtime_wide_odds_list = realtime_odds.wide_odds_list

    # 紐馬と軸馬とのワイドを購入
    for braid in braid_list:
        for axis in axis_list:
            if axis.umano == braid.umano:
                continue
            pair_num = make_wide(braid.umano, axis.umano)
            odds = list(filter(lambda real_odds: True if pair_num == real_odds.pair_umano else False, realtime_wide_odds_list))[0]
            if odds.wideodds < 25:
                continue
            bet = lowest_bet_for(2500, odds.wideodds)

            ticket_wide = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'WIDE', 'NORMAL', '', make_wide(axis.umano, braid.umano),
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
