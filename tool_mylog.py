import time

class MyLog():
    def __init__(self):
        self.log_file = r'log.txt'

    def write(self, message): #新增log
        logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(f"{logtime} {message}\n")

def test1():
    log= MyLog()
    log.write('test123中文')

if __name__ == '__main__':
    test1()
    print('ok')