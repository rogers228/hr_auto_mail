if True:
    import sys, custom_path
    config_path = custom_path.custom_path['hr_report_202208'] # 取得專案引用路徑
    sys.path.append(config_path) # 載入專案路徑
    
import pandas as pd
import pyodbc
from config import *

class db_hr(): #讀取excel 單一零件
    def __init__(self):
        self.cn = pyodbc.connect(config_conn_HR) # connect str 連接字串
        self.dbps = self.get_database_ps() # 建議一次性基本資料檔，避免多次存取db

    def get_database_ps(self):
        s = "SELECT ps01,ps02,ps03,ps11,ps12,ps14,ps23,ps31,ps32,ps33,ps34,ps52 FROM rec_ps ORDER BY ps01"
        df = pd.read_sql(s, self.cn) #轉pd
        return df

    def nogetName(self, myno): #人員編號取得姓名
        ps = self.dbps
        df = ps.loc[ps['ps02'] == myno] # 篩選
        return df.iloc[0]['ps03'] if len(df.index) > 0 else ''

    def nogetId(self, myno): #依人員列表，人員編號取得id
        ps = self.dbps
        df = ps.loc[ps['ps02'] == myno] # 篩選
        return df.iloc[0]['ps01'] if len(df.index) > 0 else ''

    def idgetps14(self, myid): #人員ID取得 ps14通知Email
        ps = self.dbps
        df = ps.loc[ps['ps01'] == myid] # 篩選
        return df.iloc[0]['ps14'] if len(df.index) > 0 else ''
        
    def runsql(self, SQL):
        try:
            cur = self.cn.cursor()
            cur.execute(SQL) #執行
            cur.commit() #更新
            cur.close() #關閉
        except:
            print(SQL)
            logging.warning('error class db_ab().def runsql()! 無法執行SQL!')

    def Get_hhk_df(self, ym, userno_arr=''):
        # ym 年月日6碼
        # userno_arr 使用者工號 AA0031,AA0094 文字陣列
        if userno_arr == "":
            userno_inSTR = ""
        else:
            userno_arr = str(userno_arr).replace(' ','') # 去除空格
            userno_inSTR = "('" + "','".join(userno_arr.split(',')) + "')"

        s = '''
            SELECT ps02,ps03,rd03,rd11,rd12
            FROM rec_rd
            LEFT JOIN rec_ps ON rd02=ps01
            WHERE
                rd03 LIKE '{0}%' AND
                rd13 = 2 AND
                rd12 NOT LIKE '%未結算%' AND
                ps11 = 1 AND
                ps34 = 1 AND
                ps14 <> ''
                WHEREPLACESTR
            '''
        # rd13 = 2 異常 rd12備註非未結算
        # ps11 = 1 在職 ps34 = 1 需要刷卡 ps14 <> '' 有Email
        s = s.format(ym)
        s = s.replace('WHEREPLACESTR','' if userno_inSTR =='' else f' AND ps02 IN {userno_inSTR}')
        df = pd.read_sql(s, self.cn) #轉pd
        return df if len(df.index) > 0 else None

def test1():
    # new id
    hr = db_hr()
    df = hr.Get_hhk_df('202208','AA0290')
    print(df)

if __name__ == '__main__':
    test1()        
    print('ok')