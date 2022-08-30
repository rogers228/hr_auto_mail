# 已加入windows排程
import os, time
import jinja2
import tool_db_hr, tool_func, tool_email, tool_mylog

def render_jinja_html(template_loc, file_name, **context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc+'/')
    ).get_template(file_name).render(context)

def main():
    currtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    ehr = tool_email.Email_HR()
    log = tool_mylog.MyLog()
    hr = tool_db_hr.db_hr()
    df = hr.Get_hhk_df(tool_func.ger_ym())
    lis_ps = list(set(df['ps02'].tolist())) #人員
    lis_ps.sort()
    for i, psno in enumerate(lis_ps):
        # print(psno, hr.nogetName(psno))
        psid = hr.nogetId(psno)
        email = hr.idgetps14(psid)
        df_w = df.loc[(df['ps02'] == psno)] # 依人員篩選
        lis = df_w.values.tolist() # data
        html = render_jinja_html(os.getcwd(), 'template_email_c.html', psno=psno, lis=lis, currtime=currtime)
        try:
            log.write(f'sendmail {psno} {email} 出勤異常通知\n{html}')
            # ehr.sendmail(email, html, '出勤異常通知') # 寄信
        except:
            log.write(f'出勤異常通知, 寄信給{psno}失敗:({email})')

if __name__ == '__main__':
    main()
    print('finished')