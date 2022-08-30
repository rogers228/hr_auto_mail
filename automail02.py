# 請假後email通知代理人

import sys, time
import tool_email
import tool_mylog
import tool_db_hr 
import tool_html
import tool_func


def in_work_time(func): # 僅工作時間內通知
    def wrap():
        h = int(time.strftime("%H", time.localtime()))
        # h = 8
        if any([h<7, h>=21]): # 8點到20點執行通知 7點前 21點後 不執行
            # print('exit')
            sys.exit()
            return
        func()
    return wrap

def get_ms_dic(dateframe_row):
    #　收件者　與　通知說明
    r = dateframe_row
    lis_ps12 = r['ps12'].split(',') if len(r['ps12']) > 0 else [] # 職務代理人
    lis_ps13 = r['ps13'].split(',') if len(r['ps12']) > 0 else [] # 簽核人
    lis_ps52 = r['ps52'].split(',') if len(r['ps12']) > 0 else [] # 請假通知人
    lis_m = [] # 所有收件者
    lis_m.extend(lis_ps12); lis_m.extend(lis_ps13); lis_m.extend(lis_ps52)
    lis_m = list(filter(lambda e: e != '', lis_m)) # 非空白
    lis_m = list(set(lis_m)) # 不重複
    # print(lis_m)
    lis_v = []
    for psno in lis_m:
        t = ''
        if psno in lis_ps13: # 簽核人
            t += ',請您撥冗至系統簽核'
        if psno in lis_ps12: # 職務代理人
            t += ',將由您代理職務請您準備'
        if psno in lis_ps52: # 請假通知人
            t += ',若影響您的工作請事先協調'
        lis_v.append(t)
    
    return dict(zip(lis_m, lis_v))

@in_work_time
def main():
    ehr = tool_email.Email_HR()
    log = tool_mylog.MyLog()
    log_file = r'log_automail02.txt'
    hr = tool_db_hr.db_hr()
    hj = tool_html.Jinja2()
    df = hr.get_sg1_test()

    # print(df)
    for i, r in df.iterrows():
        currtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        psno = r['ps02'] # 請假人
        holiday = hr.dic_sg().get(r['sg05'], '未設定假別') # 假別
        d = r['sg06']; date1 = f'{d[0:4]}-{d[4:6]}-{d[6:8]}' # 起始時間 年月日
        d = r['sg07']; date2 = f'{d[4:6]}-{d[6:8]}' # 結束時間 月日
        dg = f"{r['sg08']:.3f}"; dg = dg.rstrip('0'); dg = dg.rstrip('.') # 特別格式 小數點去除0 及 小數點
        days = dg # 請假天數 
        dic = get_ms_dic(r) # 收件者　與　通知說明
        for addressee in dic:
            message = dic[addressee] # 通知說明
            # print('currtime:', currtime) # 系統日期
            # print('addressee:', addressee) # 收件人
            # print('psno:', psno) # 收件人
            # print('message:', message) # 通知說明
            # print('holiday:', holiday) 
            # print('date1:', date1)
            # print('date2:', date2)
            # print('days:', days)
            # print('-----')
            html = hj.render_jinja_html('template_email_h.html',
                currtime = currtime,
                addressee =  addressee,
                psno = psno,
                message = message,
                holiday = holiday,
                date1=date1, date2=date2, days=days)
            try:
                log.write(log_file, f'sendmail {psno} {addressee} 請假通知\n{html}')
                # ehr.sendmail(addressee, html, '出勤異常通知') # 寄信
            except:
                log.write(log_file, f'請假通知, 寄信給{psno}失敗:({email})')

    # for i, psno in enumerate(lis_ps):
    #     psid = hr.nogetId(psno); email = hr.idgetps14(psid)
    #     df_w = df.loc[(df['ps02'] == psno)] # 依人員篩選
    #     lis = df_w.values.tolist() # data
    #     html = hj.render_jinja_html('template_email_c.html',
    #         psno=psno, lis=lis, currtime=currtime)
    #     try:
    #         log.write(log_file, f'sendmail {psno} {email} 出勤異常通知\n{html}')
    #         # ehr.sendmail(email, html, '出勤異常通知') # 寄信
    #     except:
    #         log.write(log_file, f'出勤異常通知, 寄信給{psno}失敗:({email})')

if __name__ == '__main__':
    main()
    print('finished')