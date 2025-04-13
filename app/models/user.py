# 导入必要的模块
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    用户模型类
    用于存储用户信息和认证
    """
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，唯一且不能为空
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 邮箱，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 密码哈希值
    password_hash = db.Column(db.String(128))
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户状态
    is_active = db.Column(db.Boolean, default=True)
    # 是否启用通知
    notifications_enabled = db.Column(db.Boolean, default=True)
    # Firebase Cloud Messaging令牌
    fcm_token = db.Column(db.String(255))
    
    # 关联关系
    predictions = db.relationship('Prediction', backref='user', lazy=True)  # 用户的预测记录
    locations = db.relationship('UserLocation', backref='user', lazy=True)  # 用户的位置记录
    
    def set_password(self, password):
        """
        设置用户密码
        :param password: 明文密码
        """
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """
        验证密码
        :param password: 明文密码
        :return: 密码是否正确
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        将用户对象转换为字典
        :return: 包含用户信息的字典
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'notifications_enabled': self.notifications_enabled
        } 