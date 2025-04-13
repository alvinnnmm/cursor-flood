# 导入必要的模块
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.data import HistoricalData
from app import db
from datetime import datetime, timedelta

# 创建历史数据蓝图
history_bp = Blueprint('history', __name__)

@history_bp.route('/add', methods=['POST'])
@jwt_required()
def add_historical_data():
    """
    添加历史数据
    用于记录历史洪水事件和天气数据
    """
    data = request.get_json()
    
    # 检查必需字段
    required_fields = ['location', 'date', 'rainfall', 'river_level', 'flood_occurred']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必需字段'}), 400
    
    # 创建历史数据记录
    historical_data = HistoricalData(
        location=data['location'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        rainfall=data['rainfall'],
        river_level=data['river_level'],
        flood_occurred=data['flood_occurred'],
        weather_conditions=data.get('weather_conditions', {})
    )
    
    # 保存到数据库
    db.session.add(historical_data)
    db.session.commit()
    
    return jsonify({'message': '历史数据添加成功'}), 201

@history_bp.route('/location', methods=['GET'])
@jwt_required()
def get_location_history():
    """
    获取指定位置的历史数据
    需要提供经纬度坐标
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({'error': '需要提供经纬度坐标'}), 400
    
    # 获取指定位置的历史数据
    historical_data = HistoricalData.query.filter_by(
        location={'latitude': float(latitude), 'longitude': float(longitude)}
    ).order_by(HistoricalData.date.desc()).all()
    
    return jsonify({
        'location': {'latitude': latitude, 'longitude': longitude},
        'data': [data.to_dict() for data in historical_data]
    }), 200

@history_bp.route('/analysis', methods=['GET'])
@jwt_required()
def analyze_historical_data():
    """
    分析历史数据
    计算指定时间段内的洪水统计信息
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    days = int(request.args.get('days', 30))
    
    if not latitude or not longitude:
        return jsonify({'error': '需要提供经纬度坐标'}), 400
    
    # 计算起始日期
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    # 获取指定时间段的历史数据
    historical_data = HistoricalData.query.filter_by(
        location={'latitude': float(latitude), 'longitude': float(longitude)}
    ).filter(HistoricalData.date >= start_date).all()
    
    # 计算统计数据
    total_floods = sum(1 for data in historical_data if data.flood_occurred)
    avg_rainfall = sum(data.rainfall for data in historical_data) / len(historical_data) if historical_data else 0
    avg_river_level = sum(data.river_level for data in historical_data) / len(historical_data) if historical_data else 0
    
    return jsonify({
        'location': {'latitude': latitude, 'longitude': longitude},
        'period': f'最近{days}天',
        'statistics': {
            'total_floods': total_floods,
            'flood_probability': total_floods / len(historical_data) if historical_data else 0,
            'average_rainfall': avg_rainfall,
            'average_river_level': avg_river_level
        },
        'data': [data.to_dict() for data in historical_data]
    }), 200 