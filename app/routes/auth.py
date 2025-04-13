from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    接收用户名、邮箱和密码，创建新用户
    """
    data = request.get_json()
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
        
    # 检查邮箱是否已存在
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已存在'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    # 保存到数据库
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '用户注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    验证用户名和密码，返回访问令牌和刷新令牌
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    # 验证用户和密码
    if user and user.check_password(data['password']):
        # 创建访问令牌和刷新令牌
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    return jsonify({'error': '无效的凭据'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    刷新访问令牌
    使用刷新令牌获取新的访问令牌
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/update-fcm', methods=['POST'])
@jwt_required()
def update_fcm_token():
    """
    更新用户的Firebase Cloud Messaging令牌
    用于推送通知
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
        
    user.fcm_token = data['fcm_token']
    db.session.commit()
    
    return jsonify({'message': 'FCM令牌更新成功'}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    获取用户个人信息
    需要有效的访问令牌
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
        
    return jsonify(user.to_dict()), 200 