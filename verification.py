from refund import *


class Verification:
    def __init__(self, ticket, is_hit, refund):
        self.ticket = ticket
        self.is_hit = is_hit
        self.refund = refund

    def to_string(self):
        return 'Verification=[{}, is_hit={}, refund={}]'.format(
            self.ticket.to_verification_format(), self.is_hit, self.refund)

    def to_gss_format(self):
        return [self.ticket.opdt,
                self.ticket.rcoursecd,
                self.ticket.rno,
                self.ticket.denomination,
                self.ticket.method,
                self.ticket.number,
                self.ticket.odds,
                int(self.ticket.bet_price),
                1 if self.is_hit else 0,  # 的中なら1を返す、外れなら0
                int(self.refund)]

    def to_csv(self):
        res_list = [1 if self.is_hit else 0, self.refund]
        return self.ticket.to_gss_format() + res_list


def get_verification_list(ticket_list):
    verification_list = []

    if len(ticket_list) == 0:
        return verification_list

    # 払い戻しの取得のために要素切り出し
    opdt = ticket_list[0].opdt
    rcoursecd = ticket_list[0].rcoursecd
    rno = ticket_list[0].rno

    # 単勝の払い戻し結果を取得
    tan_refund_list = get_tan_refund_list(opdt, rcoursecd, rno)

    # 複勝の払い戻し結果を取得
    fuku_refund_list = get_fuku_refund_list(opdt, rcoursecd, rno)

    # ワイドの払い戻し結果を取得
    wide_refund_list = get_wide_refund_list(opdt, rcoursecd, rno)

    # 3連複の払い戻し結果を取得
    trio_refund_list = get_trio_refund_list(opdt, rcoursecd, rno)

    for ticket in ticket_list:
        if ticket.denomination == 'TANSYO':
            verification_list.append(
                get_verification(
                    ticket, tan_refund_list))

        if ticket.denomination == 'FUKUSYO':
            verification_list.append(
                get_verification(
                    ticket, fuku_refund_list))

        if ticket.denomination == 'WIDE':
            verification_list.append(
                get_verification(
                    ticket, wide_refund_list))

        if ticket.denomination == 'TRIO':
            verification_list.append(
                get_verification(
                    ticket, trio_refund_list))

    return verification_list


# 払い戻しの中に買い目があるかどうか
def get_verification(ticket, refund_list):
    for refund in refund_list:
        if ticket.number == refund.umano:
            return Verification(ticket, True, refund.refund)
    return Verification(ticket, False, 0)
