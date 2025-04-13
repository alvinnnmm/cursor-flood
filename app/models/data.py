# 导入必要的模块
from app import db
from datetime import datetime

class Prediction(db.Model):
    """
    洪水预测模型
    存储用户的洪水预测结果
    """
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户ID，外键关联到User表
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 纬度
    latitude = db.Column(db.Float, nullable=False)
    # 经度
    longitude = db.Column(db.Float, nullable=False)
    # 预测时间
    prediction_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 洪水概率
    flood_probability = db.Column(db.Float, nullable=False)
    # 置信度分数
    confidence_score = db.Column(db.Float)
    # 风险等级（低、中、高）
    risk_level = db.Column(db.String(20))
    # 预测时的天气数据
    weather_data = db.Column(db.JSON)
    
    def to_dict(self):
        """
        将预测对象转换为字典
        :return: 包含预测信息的字典
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'prediction_time': self.prediction_time.isoformat(),
            'flood_probability': self.flood_probability,
            'confidence_score': self.confidence_score,
            'risk_level': self.risk_level,
            'weather_data': self.weather_data
        }

class SensorData(db.Model):
    """
    传感器数据模型
    存储Arduino传感器的实时数据
    """
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 设备ID
    device_id = db.Column(db.String(64), nullable=False)
    # 数据采集时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 土壤湿度
    soil_moisture = db.Column(db.Float)
    # 温度
    temperature = db.Column(db.Float)
    # 湿度
    humidity = db.Column(db.Float)
    # 降雨量
    rainfall = db.Column(db.Float)
    # 水位
    water_level = db.Column(db.Float)
    # 位置信息（经纬度）
    location = db.Column(db.JSON)
    
    def to_dict(self):
        """
        将传感器数据对象转换为字典
        :return: 包含传感器数据的字典
        """
        return {
            'id': self.id,
            'device_id': self.device_id,
            'timestamp': self.timestamp.isoformat(),
            'soil_moisture': self.soil_moisture,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'rainfall': self.rainfall,
            'water_level': self.water_level,
            'location': self.location
        }

class HistoricalData(db.Model):
    """
    历史数据模型
    存储历史洪水事件和天气数据
    """
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 位置信息（经纬度）
    location = db.Column(db.JSON, nullable=False)
    # 日期
    date = db.Column(db.Date, nullable=False)
    # 降雨量
    rainfall = db.Column(db.Float)
    # 河流水位
    river_level = db.Column(db.Float)
    # 是否发生洪水
    flood_occurred = db.Column(db.Boolean)
    # 天气状况
    weather_conditions = db.Column(db.JSON)
    
    def to_dict(self):
        """
        将历史数据对象转换为字典
        :return: 包含历史数据的字典
        """
        return {
            'id': self.id,
            'location': self.location,
            'date': self.date.isoformat(),
            'rainfall': self.rainfall,
            'river_level': self.river_level,
            'flood_occurred': self.flood_occurred,
            'weather_conditions': self.weather_conditions
        } 