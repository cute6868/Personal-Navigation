import sys
import os


def get_project_path():
    """
    :return: 返回项目的根目录
    """
    project_path = os.path.dirname(sys.argv[0])
    return project_path
