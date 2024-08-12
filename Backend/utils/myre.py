import re


# 创建一个检查者类
class Examiner(object):
    @staticmethod
    def _regular_check(pattern, target):
        """
            匹配成功：返回 True
            匹配失败：返回 False
        """
        return re.match(pattern, target) is not None

    def check_name(self, name):
        name_pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9_]{1,32}$'
        return self._regular_check(name_pattern, name)

    def check_password(self, password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
        return self._regular_check(password_pattern, password)

    def check_phone(self, phone):
        phone_pattern = r"^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$"
        return self._regular_check(phone_pattern, phone)

    def check_email(self, email):
        email_pattern = r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'
        return self._regular_check(email_pattern, email)

    # 清洗字符串（文本）
    def clean_string(slef, text):
        """
        :param text: 需要进行清洗的字符串
        :return: 清洗后的字符串内容
        清洗规则：只保留汉字，英文字母，阿拉伯数字，以及常用的中文符号，如：逗号，句号，问号，分号，冒号，感叹号，单双引号
        """
        text_pattern = r"[^\u4e00-\u9fff\u0020\u3000\w，。！？“”；‘’：a-zA-Z0-9]+"
        return re.sub(text_pattern, "", text)
