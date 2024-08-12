from utils.path import get_project_path
from json import dump
import datetime
import os

# 获取项目目录
project_path = get_project_path()

# 获取日志存放的目录
directory_path = os.path.join(project_path, 'logs')

# 获取最近操作的文件的路径
files = os.listdir(path=directory_path)
latest_file = 0
for file in files:
    num = int(file.rsplit('.', 1)[0])  # 将文件名去除后缀，并转化成int类型
    if num > latest_file:
        latest_file = num
latest_file_path = os.path.join(directory_path, f"{latest_file}.json")


# 记录日志
def record(error):
    # 声明使用全局变量
    global latest_file_path

    # 获取当前时间
    time = datetime.datetime.now()

    # 整理error数据
    information = {
        "time": time.strftime('%Y-%m-%d %H:%M:%S %A'),
        "info": str(error)
    }

    # 对最近操作的文件进行大小判断
    size = os.path.getsize(latest_file_path)

    # 如果这个文件大于2MB，则创建一个新的文件，并写入数据
    if size > int(2097152):  # 2097152B = 2MB
        new_file_path = os.path.join(directory_path, f"{time.strftime('%Y%m%d%H%M%S')}.json")
        latest_file_path = new_file_path  # 更新最近操作的文件的路径
        with open(new_file_path, 'w') as f:
            dump(information, f, indent=4)

    # 如果这个文件没有大于2MB，就直接将数据写入这个文件中
    else:
        with open(latest_file_path, 'a') as f:
            dump(information, f, indent=4)
