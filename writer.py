import os
import csv


def make_csv(ticket_list, timestamp):
    make_tickets_dir()
    with open('./tickets/ticket_' + timestamp + '.csv', 'w') as f:
        for ticket in ticket_list:
            f.write(ticket.to_csv() + '\n')


# ticketsフォルダがなかったら作成する
def make_tickets_dir():
    if not os.path.isdir('./tickets'):
        os.mkdir('./tickets')
    else:
        pass


# races以下に過去のレースのURLが記載されているtxtファイルを作成
def write_races_csv(date, url):
    path = './races/{}.txt'.format(date)
    with open(path, mode='a') as f:
        f.write(url + '\n')


def write_result_to_csv(opdt, verification_list):
    path = './verification/{}.csv'.format(opdt[0:6])
    with open(path, mode='a') as f:
        writer = csv.writer(f)
        for verification in verification_list:
            writer.writerow(verification.to_csv())
