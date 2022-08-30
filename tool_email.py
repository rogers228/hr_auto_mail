from email.mime.text import MIMEText
from email.header import Header
import smtplib
import config

class Email_HR():
    def __init__(self):
        self.account =  config.cf_email_user
        self.password = config.cf_email_pwd

    def sendmail(self, usermail, bodytext, title): # 寄信
        systemName = 'Yeoshe HR'
        user = self.account
        pwd = self.password
        server = smtplib.SMTP('smtp.hibox.biz', 25)
        server.ehlo() #回應
        server.starttls() #加密
        server.login(user, pwd) #登入
        mail = MIMEText(bodytext, 'html', 'utf-8')
        mail['From'] = '{0} <{1}>'.format(systemName, user) # Yeoshe HR <twa988@yeoshe.com.tw>
        mail['To'] = usermail
        mail['Subject'] = Header(title, 'utf-8')
        try:
            server.sendmail(user, [usermail], mail.as_string())
        except:
            pass
        server.quit()

def test1():
    mystr = '這是一封測式信件'
    ehr = Email_HR()
    ehr.sendmail('rogers2288@gmail.com', mystr,'請假通知測試')

if __name__ == '__main__':
    test1()
    print('ok')