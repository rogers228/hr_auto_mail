# 計薪前 email通知出勤異常
# 20220831 加入windows排程
import time
import tool_email
import tool_db_hr 
import tool_html
import tool_func
import tool_mylog
from functools import partial

def main():
    mylog = tool_mylog.MyLog(); log = partial(mylog.write, r'log_automail01.txt')
    currtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    ehr = tool_email.Email_HR()
    log = tool_mylog.MyLog()
    log_file = r'log_automail01.txt'
    hr = tool_db_hr.db_hr()
    hj = tool_html.Jinja2()
    df = hr.Get_hhk_df(tool_func.ger_ym())
    lis_ps = list(set(df['ps02'].tolist())) # 人員不重複
    lis_ps.sort()

    for i, psno in enumerate(lis_ps):
        psid = hr.nogetId(psno); email = hr.idgetps14(psid)
        df_w = df.loc[(df['ps02'] == psno)] # 依人員篩選
        lis = df_w.values.tolist() # data
        html = hj.render_jinja_html('template_email_c.html',
            psno=psno, lis=lis, currtime=currtime)
        try:
            log(f'sendmail {psno} {email} 出勤異常通知')
            ehr.sendmail(email, html, '出勤異常通知') # 寄信
        except:
            log(f'出勤異常通知, 寄信給{psno}失敗, email:{email}')

if __name__ == '__main__':
    main()
    print('finished')