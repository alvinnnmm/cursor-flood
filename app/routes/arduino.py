from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.data import SensorData
from app import db, mqtt
from datetime import datetime, timedelta

# 创建Arduino蓝图
arduino_bp = Blueprint('arduino', __name__)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """
    MQTT连接回调函数
    在成功连接到MQTT代理时调用
    """
    if rc == 0:
        print("成功连接到MQTT代理")
        mqtt.subscribe("flood/sensor/#")  # 订阅所有传感器主题
    else:
        print(f"连接到MQTT代理失败，错误码：{rc}")

@mqtt.on_message()
def handle_message(client, userdata, message):
    """
    MQTT消息处理函数
    处理接收到的传感器数据
    """
    try:
        # 解析消息数据
        data = message.payload.decode()
        topic = message.topic
        device_id = topic.split('/')[-1]
        
        # 创建传感器数据记录
        sensor_data = SensorData(
            device_id=device_id,
            timestamp=datetime.utcnow(),
            **data
        )
        
        # 保存到数据库
        db.session.add(sensor_data)
        db.session.commit()
        
    except Exception as e:
        print(f"处理MQTT消息时出错：{str(e)}")

@arduino_bp.route('/data', methods=['POST'])
@jwt_required()
def receive_sensor_data():
    """
    接收传感器数据
    通过HTTP POST请求接收Arduino传感器数据
    """
    data = request.get_json()
    
    if not data.get('device_id'):
        return jsonify({'error': '需要提供设备ID'}), 400
    
    # 创建传感器数据记录
    sensor_data = SensorData(
        device_id=data['device_id'],
        timestamp=datetime.utcnow(),
        soil_moisture=data.get('soil_moisture'),
        temperature=data.get('temperature'),
        humidity=data.get('humidity'),
        rainfall=data.get('rainfall'),
        water_level=data.get('water_level'),
        location=data.get('location')
    )
    
    # 保存到数据库
    db.session.add(sensor_data)
    db.session.commit()
    
    return jsonify({'message': '传感器数据接收成功'}), 201

@arduino_bp.route('/data/<device_id>', methods=['GET'])
@jwt_required()
def get_sensor_data(device_id):
    """
    获取指定设备的最新数据
    :param device_id: 设备ID
    """
    # 获取设备的最新数据
    sensor_data = SensorData.query.filter_by(device_id=device_id)\
        .order_by(SensorData.timestamp.desc())\
        .first()
    
    if not sensor_data:
        return jsonify({'error': '未找到该设备的数据'}), 404
    
    return jsonify(sensor_data.to_dict()), 200

@arduino_bp.route('/data/<device_id>/history', methods=['GET'])
@jwt_required()
def get_sensor_history(device_id):
    """
    获取指定设备的历史数据
    :param device_id: 设备ID
    """
    # 获取最近24小时的数据
    start_time = datetime.utcnow() - timedelta(days=1)
    
    sensor_data = SensorData.query.filter_by(device_id=device_id)\
        .filter(SensorData.timestamp >= start_time)\
        .order_by(SensorData.timestamp.asc())\
        .all()
    
    return jsonify({
        'device_id': device_id,
        'data': [data.to_dict() for data in sensor_data]
    }), 200 