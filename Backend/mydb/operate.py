from .db import Database
from mylog import record

# 连接数据库的必要数据
CONFIG = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'gogo',
    'charset': 'utf8'
}

# 实例化一个数据库对象
db_obj = Database(CONFIG)

# 开始连接
conn, cursor = db_obj.start_connecting()

'''
    查询小知识:
        1. 查询命令
            data = cursor.fetchone()    # 一次性获取一条数据
            data = cursor.fetchall()    # 一次性获取所有数据
            data = cursor.fetchmany(n)  # 获取n条数据
            
        2. 注意事项
            如果查询可以得到结果，则 data 是元组的形式记录查询结果
            如果查询不到结果，则 data 为 None
'''


# -------------------- 查询操作 --------------------
def query(table: str, search_by: str, search_value: str):
    """
    :param table: 要操作哪张表
    :param search_by: 通过哪个字段定位
    :param search_value: 定位的值
        ----------------------------------------
        为了防止 sql 注入问题，对于来自'用户'传递过来的数据
        我们用%占位即可，execute 会帮我们检查是否合法，同时它会自动拼接并执行 sql 命令
        ----------------------------------------
        如果在数据库中找不到该账号，则 res 为 None
        如果在数据库中找得到该账号，则 res 为 元组:
            编号 res[0]   int
            账号 res[1]   str
            密码 res[2]   str
            身份 res[3]   str
            注销 res[4]   str
            冻结 res[5]   str
            手机 res[6]   str
            昵称 res[7]   str
            邮箱 res[8]   str
            年龄 res[9]   int
            性别 res[10]  str
            介绍 res[11]  str
        ----------------------------------------
    """
    sql = f"select * from {table} where {search_by} = %s;"
    cursor.execute(sql, (search_value,))
    res = cursor.fetchone()
    return res


def mutil_query(table: str, lst: list, rows_per_page: int, page: int):
    """
    :param table: 要查找的表名
    :param lst: 以列表的形式存储要修改的字段
    :param rows_per_page: 你的每页有多少行
    :param page: 第几页
    :return: None or 元组数据
    """
    fields = ", ".join(lst)
    start = rows_per_page * (page - 1)
    length = rows_per_page
    sql = f"select {fields} from {table} limit %s, %s;"
    cursor.execute(sql, (start, length))
    return cursor.fetchall()


# -------------------- 修改操作 --------------------
def modify(table: str, search_by: str, search_value: str, modified_obj: str, modified_value: str):
    """
    :param table: 要操作哪张表
    :param search_by: 通过哪个字段定位
    :param search_value: 定位的值
    :param modified_obj: 要修改哪个字段
    :param modified_value: 修改成什么值
    :return: True or False
    """
    # 补丁开始：禁止操作"超级管理员"的数据
    if search_by == 'id' and (search_value == 1 or search_value == 2):
        return False
    if search_by == 'account' and (search_value == 'admin' or search_value == 'administrator'):
        return False
    # 补丁结束 ---------------------
    sql = f"update {table} set {modified_obj} = %s where {search_by} = %s;"
    try:
        cursor.execute(sql, (modified_value, search_value))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        record(e)
        return False


def multi_modify(table: str, search_by: str, search_value: str, dic):
    """
    :param table: 要操作哪张表
    :param search_by: 通过哪个字段定位
    :param search_value: 定位的值
    :param kwargs: 以字典的形式，传入要修改的字段和对应的值
    :return: True or False
    """
    # 补丁开始：禁止操作"超级管理员"的数据
    if search_by == 'id' and (search_value == 1 or search_value == 2):
        return False
    if search_by == 'account' and (search_value == 'admin' or search_value == 'administrator'):
        return False
    # 补丁结束 ---------------------
    lt = []
    for key, value in dic.items():
        s = f"{key} = '{value}'"
        lt.append(s)
    rule = ", ".join(lt)
    sql = f"updata {table} set {rule} where {search_by} = %s;"
    try:
        cursor.execute(sql, (search_value,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        record(e)
        return False


# -------------------- 添加操作 --------------------
def add(table: str, account: str, password: str, identity: str, unregistered: str, frozen: str, phone: str,
        username: str):
    """
    :param table: 要操作哪张表
    :param account: 添加 account 字段的值
    :param password: 添加 password 字段的值
    :param identity: 添加 identity 字段的值
    :param unregistered: 添加 unregistered 字段的值
    :param frozen: 添加 frozen 字段的值
    :param phone: 添加 phone 字段的值
    :param username: 添加 username 字段的值
    :return: True or False
    """
    sql = f"insert into {table} (account, password, identity, unregistered, frozen, phone, username) values (%s, %s, %s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql, (account, password, identity, unregistered, frozen, phone, username))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        record(e)
        return False
