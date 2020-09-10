from odds import convert_rcoursecd_num
import dbconnector as con


class Refund:
    def __init__(self, umano, refund):
        self.umano = umano
        self.refund = int(refund)

    def to_string(self):
        return 'TanResult=[umano={}, refund={}]'.format(
            self.umano,
            self.refund)


# 単勝的中馬番と払戻金のリストを作成する
def get_tan_refund_list(opdt, rcoursecd, rno):
    rcoursecd = convert_rcoursecd_num(rcoursecd)
    refund_df = con.get_data(
        """
        select
            TANNO1,
            TANRFD1,
            TANNO2,
            TANRFD2,
            TANNO3,
            TANRFD3
        from
            RFD
        where
            OPDT = {}
        and
            rcoursecd = {}
        and
            rno = {}
        """.format(opdt, rcoursecd, rno)
    )
    tan_refund_list = make_tan_refund_list(refund_df)
    return tan_refund_list


# データフレームから単勝Refundリストを作成する
def make_tan_refund_list(refund_df):
    tan_refund_list = []
    for NO in ['1', '2', '3']:
        if refund_df['TANNO' + NO][0] is None:  # 値がなかったら空
            continue
        tan_refund_list.append(Refund(
            str(refund_df['TANNO' + NO][0]).zfill(2), refund_df['TANRFD' + NO][0]))

    return tan_refund_list


# 複勝的中馬番と払戻金のリストを作成する
def get_fuku_refund_list(opdt, rcoursecd, rno):
    rcoursecd = convert_rcoursecd_num(rcoursecd)
    refund_df = con.get_data(
        """
        select
            FUKNO1,
            FUKRFD1,
            FUKNO2,
            FUKRFD2,
            FUKNO3,
            FUKRFD3,
            FUKNO4,
            FUKRFD4,
            FUKNO5,
            FUKRFD5
        from
            RFD
        where
            OPDT = {}
        and
            rcoursecd = {}
        and
            rno = {}
        """.format(opdt, rcoursecd, rno)
    )
    fuku_refund_list = make_fuku_refund_list(refund_df)
    return fuku_refund_list


# データフレームから複勝Refundリストを作成する
def make_fuku_refund_list(refund_df):
    fuku_refund_list = []
    for NO in ['1', '2', '3', '4', '5']:
        fuku_no = refund_df['FUKNO' + NO][0]
        if fuku_no is None or fuku_no == '00':
            continue
        fuku_refund_list.append(Refund(
            str(refund_df['FUKNO' + NO][0]).zfill(2), refund_df['FUKRFD' + NO][0]))

    return fuku_refund_list


# 馬連的中馬番と払戻金のリストを作成する
def get_umaren_refund_list(opdt, rcoursecd, rno):
    rcoursecd = convert_rcoursecd_num(rcoursecd)
    refund_df = con.get_data(
        """
        select
            URENNO1,
            URENRFD1,
            URENNO2,
            URENRFD2,
            URENNO3,
            URENRFD3
        from
            RFD
        where
            OPDT = {}
        and
            rcoursecd = {}
        and
            rno = {}
        """.format(opdt, rcoursecd, rno)
    )
    umaren_refund_list = make_umaren_refund_list(refund_df)
    return umaren_refund_list


# データフレームから馬連Refundリストを作成する
def make_umaren_refund_list(refund_df):
    umaren_refund_list = []
    for NO in ['1', '2', '3']:
        if refund_df['URENNO' + NO][0] is None:  # 値がなかったら空
            continue
        umaren_refund_list.append(Refund(
            add_hyphen(refund_df['URENNO' + NO][0]), refund_df['URENRFD' + NO][0]))

    return umaren_refund_list


# ワイド的中馬番と払戻金のリストを作成する
def get_wide_refund_list(opdt, rcoursecd, rno):
    rcoursecd = convert_rcoursecd_num(rcoursecd)
    refund_df = con.get_data(
        """
        select
            WIDENO1,
            WIDERFD1,
            WIDENO2,
            WIDERFD2,
            WIDENO3,
            WIDERFD3,
            WIDENO4,
            WIDERFD4,
            WIDENO5,
            WIDERFD5,
            WIDENO6,
            WIDERFD6,
            WIDENO7,
            WIDERFD7
        from
            RFD
        where
            OPDT = {}
        and
            rcoursecd = {}
        and
            rno = {}
        """.format(opdt, rcoursecd, rno)
    )
    wide_refund_list = make_wide_refund_list(refund_df)
    return wide_refund_list


# データフレームからワイドRefundリストを作成する
def make_wide_refund_list(refund_df):
    wide_refund_list = []
    for NO in ['1', '2', '3', '4', '5', '6', '7']:
        if refund_df['WIDENO' + NO][0] is None:  # 値がなかったら空
            continue
        wide_refund_list.append(Refund(
            add_hyphen(refund_df['WIDENO' + NO][0]), refund_df['WIDERFD' + NO][0]))

    return wide_refund_list


# 3連複的中馬番と払戻金のリストを作成する
def get_trio_refund_list(opdt, rcoursecd, rno):
    rcoursecd = convert_rcoursecd_num(rcoursecd)
    refund_df = con.get_data(
        """
        select
            TRIONO1,
            TRIORFD1,
            TRIONO2,
            TRIORFD2,
            TRIONO3,
            TRIORFD3
        from
            RFD
        where
            OPDT = {}
        and
            rcoursecd = {}
        and
            rno = {}
        """.format(opdt, rcoursecd, rno)
    )
    trio_refund_list = make_trio_refund_list(refund_df)
    return trio_refund_list


# データフレームから3連複Refundリストを作成する
def make_trio_refund_list(refund_df):
    trio_refund_list = []
    for NO in ['1', '2', '3']:
        if refund_df['TRIONO' + NO][0] is None:  # 値がなかったら空
            continue
        trio_refund_list.append(Refund(add_hyphen_hyphen(
            refund_df['TRIONO' + NO][0]), refund_df['TRIORFD' + NO][0]))

    return trio_refund_list


def add_hyphen(wideno):
    return wideno[:2] + '-' + wideno[2:]


def add_hyphen_hyphen(triono):
    return triono[:2] + '-' + triono[2:4] + '-' + triono[4:6]
