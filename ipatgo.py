import os


def vote(timestamp):
    try:
        return os.system(
            r'ipatgo.exe file %IPATGO% .\tickets\ticket_' +
            timestamp +
            '.csv')

    except Exception as e:
        print(e.args)
        return 1

# 購入限度額を取得
def get_limit_vote_amount():
    try:
        os.system(r'ipatgo.exe stat %IPATGO%')
        path = 'C:\\umagen\\ipatgo\\stat.ini'
        with open(path) as f:
            s = f.readlines()
            for line in s:
                if (line.startswith('limit_vote_amount')):
                    return int(line.replace('limit_vote_amount=', ''))
        return 0

    except Exception as e:
        print(e.args)
        return 0