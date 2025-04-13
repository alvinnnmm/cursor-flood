from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.data import Prediction
from app.models.user import User
from app import db
from datetime import datetime
import requests
import os

predictions_bp = Blueprint('predictions', __name__)

def get_weather_data(latitude, longitude):
    """
    获取指定位置的天气数据
    :param latitude: 纬度
    :param longitude: 经度
    :return: 天气数据字典
    """
    # 从环境变量获取天气API密钥
    api_key = os.environ.get('WEATHER_API_KEY')
    # 构建API请求URL
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    return response.json()

def predict_flood_risk(weather_data, historical_data):
    """
    预测洪水风险
    :param weather_data: 天气数据
    :param historical_data: 历史数据
    :return: 洪水概率和风险等级
    """
    # 从天气数据中提取关键指标
    rainfall = weather_data.get('rain', {}).get('1h', 0)
    temperature = weather_data.get('main', {}).get('temp', 0)
    humidity = weather_data.get('main', {}).get('humidity', 0)
    
    # 简单的风险计算（实际应用中应使用机器学习模型）
    risk_score = (rainfall * 0.4) + (humidity * 0.3) + (temperature * 0.3)
    probability = min(risk_score / 100, 1.0)
    
    # 根据概率确定风险等级
    if probability < 0.3:
        risk_level = 'low'
    elif probability < 0.7:
        risk_level = 'medium'
    else:
        risk_level = 'high'
        
    return probability, risk_level

@predictions_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """
    获取洪水预测
    需要提供经纬度坐标
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({'error': '需要提供经纬度坐标'}), 400
    
    # 获取天气数据
    weather_data = get_weather_data(latitude, longitude)
    
    # 获取该位置的历史数据
    historical_data = HistoricalData.query.filter_by(
        location={'latitude': latitude, 'longitude': longitude}
    ).all()
    
    # 进行预测
    probability, risk_level = predict_flood_risk(weather_data, historical_data)
    
    # 存储预测结果
    prediction = Prediction(
        user_id=current_user_id,
        latitude=latitude,
        longitude=longitude,
        flood_probability=probability,
        risk_level=risk_level,
        weather_data=weather_data
    )
    
    db.session.add(prediction)
    db.session.commit()
    
    return jsonify({
        'prediction': prediction.to_dict(),
        'risk_level': risk_level,
        'probability': probability
    }), 200

@predictions_bp.route('/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    """
    获取用户的预测历史
    按时间倒序排列
    """
    current_user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=current_user_id)\
        .order_by(Prediction.prediction_time.desc()).all()
    
    return jsonify({
        'predictions': [pred.to_dict() for pred in predictions]
    }), 200

@predictions_bp.route('/alert', methods=['POST'])
@jwt_required()
def send_alert():
    """
    发送洪水警报
    需要用户已设置FCM令牌
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user = User.query.get(current_user_id)
    if not user or not user.fcm_token:
        return jsonify({'error': '用户不存在或未设置FCM令牌'}), 404
    
    # 这里实现实际的推送通知逻辑
    # 使用Firebase Cloud Messaging或其他推送服务
    
    return jsonify({'message': '警报发送成功'}), 200 