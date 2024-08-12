import pymysql  # 通过PyMySQL包连接到MySQL数据库


class Connect(object):

    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __str__(self):
        """

        :return:
        """
        return f"| {self.user} | {self.password} | {self.host} | {self.port} |"


class Database(object):

    def __init__(self, config):
        """
        :param config:
            格式如下：
            config = {
                'user': 'root',
                'password': 123456,
                'host': '127.0.0.1',
                'port': 3306,
                'database': 'gogo',
                'charset': 'utf8'
            }
        """
        self.link = Connect(
            config.get('user'),
            config.get('password'),
            config.get('host'),
            config.get('port')
        )
        self.name = config.get('database')
        self.charset = config.get('charset')

    def start_connecting(self):
        # 创建数据库连接
        conn = pymysql.connect(
            user=self.link.user,
            password=self.link.password,
            host=self.link.host,
            port=self.link.port,
            database=self.name,
            charset=self.charset
        )
        # 生成游标对象 cursor
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def end_connecting(conn, cursor):
        cursor.close()  # 关闭游标对象 cursor
        conn.close()  # 关闭数据库连接，释放资源
        return True
