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

def format_d12(date1, date2):
    # date1, date2 請假起迄日14碼日期 格式化 
    a, b = date1, date2
    ay,am,ad,ah,an,ae = a[0:4],a[4:6],a[6:8],a[8:10],a[10:12],a[12:14]
    by,bm,bd,bh,bn,be = b[0:4],b[4:6],b[6:8],b[8:10],b[10:12],b[12:14]
    f1 = f'{ay}-{am}-{ad} {ah}:{an}'
    f2 = f'{by}-{bm}-{bd} {ah}:{an}' if ay!=by else (
        f'{bm}-{bd} {bh}:{bn}' if a[4:8]!=b[4:8] else f'{bh}:{bn}')
    return f'{f1} ~ {f2}'

def test1():
    print(format_d12(
        '20220830080000','20220830173000'))

if __name__ == '__main__':
    test1()