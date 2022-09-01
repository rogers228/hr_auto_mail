# 請假後email通知代理人
# 20220831 加入windows排程
import sys, time
import tool_email
import tool_db_hr 
import tool_html
import tool_func
import tool_mylog
from functools import partial
mylog = tool_mylog.MyLog(); log = partial(mylog.write, r'log_automail02.txt')

def in_work_time(func): # 僅工作時間內通知
    global log
    def wrap():
        h = int(time.strftime("%H", time.localtime()))
        if any([h<=7, h>=21]): # 8點到20點執行通知 7點前 21點後 不執行
            log('非工作時間故不執行通知')
            sys.exit()
            return
        func()
    return wrap

def get_ms_dic(dateframe_row):
    #　收件者　與　通知說明內文
    r = dateframe_row
    lis_ps12 = r['ps12'].split(',') if len(r['ps12']) > 0 else [] # 職務代理人
    lis_ps13 = r['ps13'].split(',') if len(r['ps12']) > 0 else [] # 簽核人
    lis_ps52 = r['ps52'].split(',') if len(r['ps12']) > 0 else [] # 請假通知人
    lis_m = [] # 所有收件者
    lis_m.extend(lis_ps12); lis_m.extend(lis_ps13); lis_m.extend(lis_ps52)
    lis_m = list(filter(lambda e: e != '', lis_m)) # 非空白
    lis_m = list(set(lis_m)) # 不重複

    lis_v = []
    for psno in lis_m:
        t = ''
        if psno in lis_ps13: # 收件人 具簽核人身分
            t += ',請您撥冗至系統簽核'
        if psno in lis_ps12: # 收件人 具職務代理人身分
            t += ',將由您代理職務請您準備'
        if psno in lis_ps52: # 收件人 具請假通知人身分
            t += ',若影響您的工作請事先協調'
        lis_v.append(t)

    return dict(zip(lis_m, lis_v))

@in_work_time # 僅工作時間內執行通知
def main():
    global log
    ehr = tool_email.Email_HR()
    hr = tool_db_hr.db_hr()
    hj = tool_html.Jinja2()
    df = hr.get_sg1_df() # data 可更換資料來源
    if df is None:
        log('無請假需要通知')
        sys.exit() #正式結束程式  需要導入sys
        return

    for i, r in df.iterrows():
        currtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        sgid = r['sg01'] # 請假id
        psno = r['ps02'] # 請假人
        psname = hr.nogetName(psno)
        holiday = hr.dic_sg().get(r['sg05'], '未設定假別') # 假別
        date_stage = tool_func.format_d12(r['sg06'], r['sg07']) # 請假時間
        dg = f"{r['sg08']:.3f}"; dg = dg.rstrip('0'); dg = dg.rstrip('.'); days = dg # 請假天數 特別格式 小數點去除0 及 小數點
        dic = get_ms_dic(r) # 收件者與通知說明
        for addressee in dic:
            addressee_name = hr.nogetName(addressee)
            psid = hr.nogetId(addressee); email = hr.idgetps14(psid)
            message = dic[addressee] # 通知說明
            msgStr = f"請假通知:Dear{addressee}{addressee_name}:\n{psno}{psname}已申請{holiday}({sgid})於{date_stage}合計:{days}天{message}。"
            html = hj.render_jinja_html('template_email_h.html',
                currtime = currtime,
                addressee =  addressee,
                psno = psno,
                message = message,
                holiday = holiday,
                date_stage=date_stage, days=days) # 渲染
            try:
                ehr.sendmail(email, html, '請假通知') # 寄信
                log(f'sendmail: {email} {msgStr}')
            except:
                log(f'請假通知, 寄信給{addressee}失敗, email:{email}')
            finally:
                try:
                    hr.update_sg15_1(sgid) # 更新為已通知 不再通知
                    log('更新為已通知 不再通知')
                except:
                    log('error!無法更新')


if __name__ == '__main__':
    main()
    print('finished')