import threading
import time
import os

# linux shell 命令
# shell_command = "./test.sh"
shell_command = "./auto_git.sh"

# 定时运行点
timing = 20


def log(*args, **kwargs):
    """
    写入log.txt文件，带有输出时间
    """
    format = '%Y%m%d-%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print("log:", dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def shell(command):
    run_command = os.popen(command).read()
    log(run_command)


def main():
    shell(shell_command)
    global timer
    timer = threading.Timer(86400, main)
    timer.start()


def running_time(hour):
    """
    :hour: 需要定位到的时间点，小时
    :return: bool
    """
    now_time = time.localtime(time.time())
    if now_time.tm_hour == hour:
        return True
    else:
        return False


def is_right_time():
    """
    检测时间是否到点了
    """
    global timer_check_time
    timer_check_time = threading.Timer(60, is_right_time)
    # print('当前线程数为{}'.format(threading.activeCount()))
    if running_time(timing) is not True:
        log(f"not a good time ---> 等待 {timing} 点")
        timer_check_time.start()
    else:
        timer_check_time.cancel()
        main() 

def del_log():
    if os.path.exists('log.txt'):
        os.remove('log.txt')


if __name__ == '__main__':
    # main()
    del_log()
    is_right_time()
