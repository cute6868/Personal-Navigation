from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

"""
    方式一：'100 per day'、'20 per hour'、'5 per minute'、'1 per second'
    方式二：'100/day'、'20/hour'、'5/minute'、'1/second'
    两种方式作用相同，推荐方式二
"""

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/minute"]
)
