from flask import Flask
import os
from datetime import timedelta
from ext import limiter


# 创建 Flask 应用
def create_app():
    app = Flask(__name__)

    # 配置全局流量控制，所有接口都生效
    limiter.init_app(app)

    # 配置 session
    secret_key = os.urandom(24)  # 生成一个包含随机字符的字符串
    app.config['SECRET_KEY'] = secret_key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置1天有效

    # 导入蓝图
    from .views.base import bp as bp0
    from .views.manage import bp as bp1
    from .views.user import bp as bp2

    # 注册蓝图
    app.register_blueprint(bp0)
    app.register_blueprint(bp1)
    app.register_blueprint(bp2)

    return app
