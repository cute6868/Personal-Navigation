from App import create_app

if __name__ == '__main__':
    # 创建 WSGI 应用
    app = create_app()
    app.run(port=34567, host='0.0.0.0')
