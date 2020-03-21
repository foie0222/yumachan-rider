class Ticket:
    def __init__(self, opdt, rcourcecd, rno, denomination, method, multi, number, bet_price):
        self.opdt = opdt
        self.rcourcecd = rcourcecd
        self.rno = rno
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


def make_ticket(entry, realtime_odds_list):
    ticlet_list = []
    axis_list = [entry.horse_list[0]]  # 1番高確率馬は軸馬に入れておく
    braid_list = []  # 紐馬には何も入れない

    # 軸馬（上位5頭のうち軸のサインがある、もしくは単勝回収率110%以上）の単勝を購入
    for horse in entry.horse_list[:4]:
        bet = 0
        odds = list(filter(lambda realtime_odds: True if realtime_odds.umano == horse.umano else False, realtime_odds_list))[0]
        print(type(odds))

        if horse.sign == 'axis':
            bet += 500  # 軸馬だったら500円ベット
        if horse.probability * odds.tanodds >= 110:
            bet += 100  # 単勝回収率が110%以上なら追加で100円ベット
        if horse.probability * odds.tanodds >= 120:
            bet += 200  # 単勝回収率が120%以上なら追加で200円ベット
        if horse.probability * odds.tanodds >= 130:
            bet += 300  # 単勝回収率が120%以上なら追加で200円ベット

        if bet == 0:  # betが0なら次へ
            continue
        ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket)
        axis_list.append(horse)

    # 紐馬（紐のサインがある、もしくは単勝回収率170%以上）の単勝・複勝を購入
    for horse in entry.horse_list:
        bet = 0
        odds = list(filter(lambda realtime_odds: True if realtime_odds.umano == horse.umano else False, realtime_odds_list))[0]

        if horse.sign == 'braid' or horse.probability * odds.tanodds >= 170:
            bet += 100

        if bet == 0:  # betが0なら次へ
            continue
        ticket_tan = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, str(bet))
        ticket_fuku = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'FUKUSYO', 'NORMAL', '', horse.umano, str(bet))
        ticlet_list.append(ticket_tan)
        ticlet_list.append(ticket_fuku)
        braid_list.append(horse)

    # 紐馬と軸馬とのワイドを購入
    for braid in braid_list:
        for axis in axis_list:
            ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'WIDE', 'NORMAL', '', make_wide(axis.umano, braid.umano),
                            '200')
            ticlet_list.append(ticket)

    return ticlet_list


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
