class Horse:
    def __init__(self, umano, probability, sign):
        self.umano = umano.replace(' ', '0') #1桁目を0埋め
        self.probability = probability
        self.sign = sign

    def to_string(self):
        return 'Horse=[umano={}, probability={}, sign={}]'.format(self.umano, self.probability, self.sign)


def get_horse_list(txt):
    horse_list = []

    remove_tag_txt = txt.replace('<p>', '').replace('</p>', '')
    row_horse_list = remove_tag_txt.split('<br/>')

    for row_house in row_horse_list[:-1]:
        horse_list.append(Horse(row_house[1:3], row_house[4:8], get_sign(row_house)))

    return horse_list


def get_sign(row_house):
    if '軸' in row_house:
        return 'axis'
    if '紐' in row_house:
        return 'braid'
    return None


# if __name__ == '__main__':
#     get_horse_list()
