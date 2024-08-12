from flask import Blueprint
from utils import check_login_status
from ext import limiter

from ..assist.assist_user import (get_user_data, update_user_data)

# 管理部分
# -- 包含功能：
#   1. 查询个人数据
#   2. 修改个人数据


# 创建蓝图
bp = Blueprint('user', __name__, url_prefix='/user')


# 查询个人数据
@bp.route('/getdata', methods=['GET'])
@check_login_status
def getdata():
    return get_user_data()


# 更新/修改个人数据
@bp.route('/update', methods=['POST'])
@limiter.limit('10/minute', override_defaults=False)
@check_login_status
def update():
    return update_user_data()
