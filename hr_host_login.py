# 由排程觸發執行
import subprocess
import PySimpleGUI as sg

def main():
    try:
        # 新進程
        subprocess.run([r'C:\Windows\System32\mstsc.exe', r'C:\Users\user\Desktop\yshr.asuscomm.com.rdp'], check=True)
    except:
        msgbox('遠端登入hr主機執行錯誤!')

def msgbox(message, title = 'Python'):
    sg.theme('SystemDefault')
    layout = [  [sg.Text(message)],
                [sg.Text('')],
                [sg.Button('ok')] ]
    w = sg.Window(title, layout, 
                    size=(300, 120),
                    resizable=True)
    while True:
        event, values = w.read()
        if event == sg.WIN_CLOSED or event == 'ok': # if user closes window or clicks cancel
            break

def test1():
    msgbox('test!')

if __name__ == '__main__':
    test1()