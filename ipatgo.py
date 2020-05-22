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
