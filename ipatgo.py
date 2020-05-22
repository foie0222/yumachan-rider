import os


def vote():
    try:
        os.system(r'ipatgo.exe file %IPATGO% .\\tickets\\ticket_%TIMESTAMP%.csv')
        return True

    except Exception as e:
        print(e.args)
        return False
