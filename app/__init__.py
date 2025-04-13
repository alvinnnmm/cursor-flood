# 导入必要的Flask扩展和模块
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mqtt import Mqtt
from config import config

# 初始化数据库和扩展
db = SQLAlchemy()  # 数据库对象
migrate = Migrate()
jwt = JWTManager()  # JWT认证管理器
mqtt = Mqtt()  # MQTT客户端，用于Arduino通信

def create_app(config_name):
    """
    创建Flask应用实例的工厂函数
    :param config_name: 配置名称
    :return: Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask('x_flood')
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)  # 初始化数据库
    migrate.init_app(app, db)
    jwt.init_app(app)  # 初始化JWT
    CORS(app)  # 启用跨域资源共享
    mqtt.init_app(app)  # 初始化MQTT客户端
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 注册蓝图（路由模块）
    from app.routes.auth import auth_bp  # 认证相关路由
    from app.routes.predictions import predictions_bp  # 预测相关路由
    from app.routes.arduino import arduino_bp  # Arduino相关路由
    from app.routes.history import history_bp  # 历史数据相关路由
    
    # 注册蓝图并设置URL前缀
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(arduino_bp, url_prefix='/api/arduino')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    
    return app 