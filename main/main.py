import re
import logging
import os
import zipfile
import time


def month(m):
    li = ["January", "February", "March", "April", "May", "June",
          "July", "September", "October", "November", "December"]
    return li[m - 1]


if not os.path.exists("log"):
    os.makedirs("log")
else:
    localtime = time.localtime()
    year = localtime.tm_year
    mon = month(localtime.tm_mon)
    day = localtime.tm_mday
    hour = localtime.tm_hour
    mini = localtime.tm_min
    titleX = "log\\exchange{0}y{1}{2}d{3}h{4}min{5}sec.zip".format(year, mon, day, hour, mini,
                                                                   str(localtime.tm_sec + time.time() % 1))
    jungle_zip = zipfile.ZipFile(titleX, 'w')
    jungle_zip.write('log\\exchange_log.log', compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(fmt="%(name)s: %(asctime)s - %(levelname)s: %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(fmt)
sh.setLevel(logging.INFO)
fh = logging.FileHandler("log/exchange_log.log", "w", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
logger.addHandler(sh)
logger.addHandler(fh)


print("""
0V 01C 002F 0002D版本
b/B/0代表二进制
o/O/1代表八进制
d/D/10代表十进制
h/H/16代表十六进制
输入的三个参数用两个空格分开，
第一个是初始数值，不用加任何前缀
第二个是初始类型，用上面的表示，
第三个是您要转换成的类型，用上面的表示
""")


def f(v=""):
    if (v == "b") or (v == "B"):
        return 0
    elif (v == "o") or (v == "O"):
        return 1
    elif (v == "d") or (v == "D"):
        return 2
    elif (v == "h") or (v == "H"):
        return 3


def _f(v=0):
    if v == 0:
        return 2
    elif v == 1:
        return 8
    elif v == 2:
        return 10
    elif v == 3:
        return 16


while True:
    num = input("Please input the number and type, split with two space:")
    num = num.split("  ")  # 转化成两个部分，第一部分是数字，第二部分是格式，第三部分是转换后的格式
    logger.debug(f"You input:{num}")
    if num[0] == '':  # 输入不能为空
        logger.warning("请输入数字")
        continue

    number = num[0]
    if bool(re.search("[^0-9a-fA-F]", str(number))):
        logger.warning("请输入一个整数")
        continue
    try:
        t = f(num[1])
    except IndexError:
        tl = [True, True, True, True]
        for s in str(number):
            if tl[0] and bool(re.match("[^0-1]", s)):
                tl[0] = False
            if tl[1] and bool(re.match("[^0-7]", s)):
                tl[1] = False
            if tl[2] and bool(re.match("[^0-9]", s)):
                tl[2] = False
            if tl[3] and bool(re.match("[^0-9a-fA-F]", s)):
                tl[3] = False
        if tl[2] and (not tl[0]):
            t = 2
        else:
            t = tl.index(True)
    try:
        t_to = f(num[2])
    except IndexError:
        if t != 0:
            t_to = 0
        else:
            t_to = 2

    logger.info(f"智能判断为{t} -- {t_to}")
    try:
        out = int(str(number), _f(t))
    except ValueError:
        logger.warning("指示错误")
        continue
    if t_to == 0:
        out = bin(out)
    elif t_to == 1:
        out = oct(out)
    elif t_to == 3:
        out = hex(out)
    logger.exception(f"从{number}转换成{out}")

