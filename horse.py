import re

from images import save_png, img_to_base64, request_cloud_vison_api


class Horse:
    def __init__(self, umano, probability):
        self.umano = umano
        self.probability = probability

    def to_string(self):
        return 'Horse=[umano={}, probability={}]'.format(
            self.umano, self.probability)


def get_horse_list(txt):
    horse_list = []

    remove_tag_txt = txt.replace('<p>', '').replace('</p>', '')
    row_horse_list = remove_tag_txt.split('<br/>')

    for row_house in row_horse_list[:-1]:
        horse_list.append(
            Horse(
                get_hotse_no(row_house),
                get_probability(row_house),
            ))

    return horse_list


def get_horse_list_from_png_by_google(image_url):
    horse_list = []

    # 画像を保存
    save_png(image_url)

    # 文字認識させたい画像を取得
    img_base64 = img_to_base64('./image/source.png')
    result = request_cloud_vison_api(img_base64)

    # 認識した文字のみを出力
    text_r = result["responses"][0]["fullTextAnnotation"]["text"]
    lines = text_r.split('\n')
    for line in lines:
        if is_invalid(line):
            continue
        horse_list.append(
            Horse(
                get_hotse_no_by_png(line),
                get_probability_by_png(line)))

    return horse_list


def is_invalid(line):
    if len(line) < 6:  # 6文字未満の読み込み行は無効に
        return True

    if ('(' in line):
        index = line.index('(')
    if ('【' in line):
        index = line.index('【')
    if ('[' in line):
        index = line.index('[')

    if not bool(re.search(r'\d', line[:index + 1])):
        return True

    return False


def get_hotse_no_by_png(line):
    line = line[0:5]
    if ('(' in line):
        index = line.index('(')
    elif ('【' in line):
        index = line.index('【')
    elif ('[' in line):
        index = line.index('[')

    no = int(re.sub('\\D', '', line[:index + 1]))
    return str(no).zfill(2)  # 0埋め


def get_probability_by_png(line):
    end_line = line
    if ('(' in end_line):
        index = end_line.index('(')
    elif ('【' in end_line):
        index = end_line.index('【')
    elif ('[' in end_line):
        index = end_line.index('[')

    probability = float(end_line[index + 1:end_line.index('%')])
    return probability


def get_hotse_no(row_house):
    return row_house[1:3].replace(' ', '0')  # 1桁目がブランクの場合は0埋め


def get_probability(row_house):
    return float(row_house[4:8])
