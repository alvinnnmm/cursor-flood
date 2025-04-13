# 导入必要的模块
import os
from datetime import timedelta

class Config:
    """
    应用配置类
    包含所有配置设置
    """
    # Flask设置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'  # 密钥
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'  # 环境
    
    # 数据库设置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/x_flood'  # 数据库连接URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用SQLAlchemy事件系统
    
    # JWT设置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'  # JWT密钥
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 访问令牌有效期
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 刷新令牌有效期
    
    # CORS设置
    CORS_HEADERS = 'Content-Type'  # 允许的CORS头
    
    # MQTT设置
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL') or 'localhost'  # MQTT代理地址
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT') or 1883)  # MQTT代理端口
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')  # MQTT用户名
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')  # MQTT密码
    
    # Firebase设置
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS')  # Firebase凭证
    
    # 模型设置
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/x_flood_model.h5')  # 模型文件路径
    
    # 上传设置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  # 上传文件目录
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大文件大小（16MB） 