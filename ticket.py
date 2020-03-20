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


def make_ticket(entry):
    ticlet_list = []

    # 軸馬の単勝を購入
    for horse in entry.horse_list:
        if horse.sign == 'axis':
            ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, '500')
            ticlet_list.append(ticket)

    # 紐馬の単勝を購入
    for horse in entry.horse_list:
        if horse.sign == 'braid':
            ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'TANSYO', 'NORMAL', '', horse.umano, '100')
            ticlet_list.append(ticket)

    # 紐馬は1番人気馬と軸馬とのワイドを購入
    for horse in entry.horse_list:
        axis_list = get_axis_list(entry.horse_list)
        if horse.sign == 'braid':
            for axis in axis_list:
                ticket = Ticket(entry.opdt, entry.rcourcecd, entry.rno, 'WIDE', 'NORMAL', '', axis.umano + '-' + horse.umano,
                                '200')
                ticlet_list.append(ticket)

    for ticket in ticlet_list:
        print(ticket.to_string())

    return ticlet_list


# 軸馬と1番高確率の馬のリスト
def get_axis_list(horse_list):
    axis_list = [horse_list[0]]

    for horse in horse_list:
        if horse.sign == 'axis':
            axis_list.append(horse)

    return axis_list
