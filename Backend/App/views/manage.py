from flask import Blueprint, request, jsonify

from utils.decorator import (check_login_status, check_admin_permission)

from ..assist.assist_manage import (set_field, search_data)

# 管理部分
# -- 包含功能：
#   1. 添加管理员权限
#   2. 移除管理员权限
#   3. 冻结账号
#   4. 取消冻结
#   5. 恢复已注销账号
#   6. 查询用户表数据

# 创建蓝图
bp = Blueprint('manage', __name__, url_prefix='/manage')


# 添加管理员权限
@bp.route('/add', methods=['POST'])
@check_login_status
@check_admin_permission
def add_admin_privilege():
    return set_field('identity', '1', '添加管理员权限成功！')


# 移除管理员权限
@bp.route('/remove', methods=['POST'])
@check_login_status
@check_admin_permission
def remove_admin_privilege():
    return set_field('identity', '0', '移除管理员权限成功！')


# 冻结账号
@bp.route('/freeze', methods=['POST'])
@check_login_status
@check_admin_permission
def freeze_account():
    return set_field('frozen', '1', '冻结成功！')


# 取消冻结
@bp.route('/unfreeze', methods=['POST'])
@check_login_status
@check_admin_permission
def unfreeze_account():
    return set_field('frozen', '0', '取消冻结成功！')


# 恢复已注销账号
@bp.route('/restore', methods=['POST'])
@check_login_status
@check_admin_permission
def restore_account():
    return set_field('unregistered', '0', '恢复已注销账号成功！')


# 查询用户表数据
@bp.route('/table', methods=['GET'])
@check_login_status
@check_admin_permission
def get_user_table():
    row = request.get_json().get('row')
    page = request.get_json().get('page')
    if not (row and page):
        return jsonify(msg='数据不齐全！', data=[], code=0)
    if not (row.isdigit() and page.isdigit()):
        return jsonify(msg='请输入数值！', data=[], code=0)
    return search_data(int(row), int(page))
