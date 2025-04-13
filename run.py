from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("启动 X Flood 洪水预测系统...")
    app.run(host='0.0.0.0', port=5000) 