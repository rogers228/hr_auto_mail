# 已加入windows排程
import time

def ger_ym(): #依照日期取得查詢年月
    #若為15號以前，取得上個月的年與月
    #若為15號以後，取得這個月的年與月
    currY = int(time.strftime('%Y', time.localtime()))
    currM = int(time.strftime('%m', time.localtime()))
    currD = int(time.strftime('%d', time.localtime()))
    if currD < 15:
        if currM == 1:
            cY, cM = currY-1, 12
        else:
            cY, cM = currY, currM - 1
    else:
        cY, cM = currY, currM

    return f'{cY:0>2d}{cM:0>2d}'

def test1():
    print(ger_ym())

if __name__ == '__main__':
    test1()