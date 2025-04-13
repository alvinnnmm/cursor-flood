import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from datetime import datetime
import re
import matplotlib.pyplot as plt
import seaborn as sns
import serial
import time
import webbrowser
from geopy.distance import geodesic

class FloodPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.esp32_port = None
        self.esp32_baudrate = 9600
        
        # 设置安全屋坐标
        self.safe_house_coords = (2.3421294367516348, 111.84346739065093)
        
        # 设置阈值
        self.thresholds = {
            'Temperature (°F)': 90,  # 温度阈值
            'Humidity (%)': 80,      # 湿度阈值
            'Wind Speed (mph)': 15,  # 风速阈值
            'Pre': 29.7             # 气压阈值
        }
        
        # 设置当前位置（示例坐标，需要根据实际情况更新）
        self.current_location = (2.3421294367516348, 111.84346739065093)
        
    def load_data(self, file_path):
        """加载天气数据"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            print(f"成功加载数据，共 {len(df)} 条记录")
            
            # 显示所有列名
            print("\nExcel文件中的列名:")
            print(df.columns.tolist())
            
            print("\n数据预览:")
            print(df.head())
            
            return df
        except Exception as e:
            print(f"加载数据时出错: {str(e)}")
            return None

    def analyze_weather_patterns(self, df):
        """分析天气模式"""
        try:
            # 创建图表目录
            os.makedirs('analysis_plots', exist_ok=True)
            
            # 计算统计信息
            print("\n天气数据统计:")
            for column in df.columns:
                if df[column].dtype in ['int64', 'float64']:
                    print(f"\n{column}统计:")
                    print(f"平均值: {df[column].mean():.2f}")
                    print(f"最大值: {df[column].max():.2f}")
                    print(f"最小值: {df[column].min():.2f}")
                    print(f"标准差: {df[column].std():.2f}")
                    
                    # 绘制分布图
                    plt.figure(figsize=(10, 6))
                    sns.histplot(data=df, x=column, bins=20)
                    plt.title(f'{column}分布')
                    plt.savefig(f'analysis_plots/{column}_distribution.png')
                    plt.close()
            
            # 分析变量之间的关系
            plt.figure(figsize=(12, 8))
            sns.pairplot(df[['Temperature (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pre']])
            plt.savefig('analysis_plots/variable_relationships.png')
            plt.close()
            
            return True
        except Exception as e:
            print(f"分析天气模式时出错: {str(e)}")
            return False

    def preprocess_data(self, df):
        """预处理数据"""
        try:
            # 选择特征
            features = ['Temperature (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pre']
            
            # 标准化特征
            X = df[features]
            X_scaled = self.scaler.fit_transform(X)
            
            # 创建洪水风险标签（示例：基于湿度和降雨量的组合）
            df['Flood_Risk'] = (df['Humidity (%)'] * 0.4 + 
                              (df['Pre'] - df['Pre'].min()) / (df['Pre'].max() - df['Pre'].min()) * 0.6)
            
            y = df['Flood_Risk']
            
            return X_scaled, y
        except Exception as e:
            print(f"预处理数据时出错: {str(e)}")
            return None, None

    def train_model(self, X, y):
        """训练模型"""
        try:
            # 使用5折交叉验证
            kf = KFold(n_splits=5, shuffle=True, random_state=42)
            self.model = RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            )
            
            # 进行交叉验证
            cv_scores = cross_val_score(self.model, X, y, cv=kf, scoring='neg_mean_squared_error')
            print("\n交叉验证结果:")
            print(f"平均MSE: {-cv_scores.mean():.2f}")
            print(f"标准差: {cv_scores.std():.2f}")
            print(f"各折MSE: {-cv_scores}")
            
            # 训练最终模型
            self.model.fit(X, y)
            
            # 获取特征重要性
            feature_importance = pd.DataFrame({
                'feature': ['Temperature', 'Humidity', 'Wind Speed', 'Pressure'],
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n特征重要性:")
            print(feature_importance)
            
            # 计算R²分数
            y_pred = self.model.predict(X)
            r2 = r2_score(y, y_pred)
            print(f"\n模型R²分数: {r2:.2f}")
            
            return True
        except Exception as e:
            print(f"训练模型时出错: {str(e)}")
            return False

    def connect_esp32(self, port='COM3'):
        """连接ESP32"""
        try:
            self.esp32_port = serial.Serial(port, self.esp32_baudrate, timeout=1)
            print(f"成功连接到ESP32，端口: {port}")
            return True
        except Exception as e:
            print(f"连接ESP32时出错: {str(e)}")
            return False

    def check_thresholds(self, data):
        """检查是否超过阈值"""
        alerts = []
        for key, value in data.items():
            if key in self.thresholds:
                if key == 'Pre' and value < self.thresholds[key]:
                    alerts.append(f"{key} 低于阈值: {value} < {self.thresholds[key]}")
                elif key != 'Pre' and value > self.thresholds[key]:
                    alerts.append(f"{key} 超过阈值: {value} > {self.thresholds[key]}")
        return alerts
    
    def navigate_to_safe_house(self):
        """导航到安全屋"""
        try:
            # 计算距离
            distance = geodesic(self.current_location, self.safe_house_coords).kilometers
            
            # 生成Google Maps导航链接
            url = f"https://www.google.com/maps/dir/?api=1&destination={self.safe_house_coords[0]},{self.safe_house_coords[1]}"
            
            print(f"\n紧急情况！请立即前往安全屋！")
            print(f"安全屋距离: {distance:.2f} 公里")
            print(f"正在打开导航...")
            
            # 打开导航
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"导航时出错: {str(e)}")
            return False

    def update_current_location(self, lat, lon):
        """更新当前位置"""
        self.current_location = (lat, lon)
        print(f"当前位置已更新: {lat}, {lon}")

    def get_esp32_data(self):
        """从ESP32获取数据"""
        try:
            if self.esp32_port and self.esp32_port.is_open:
                # 读取一行数据
                data = self.esp32_port.readline().decode('utf-8').strip()
                if data:
                    # 解析数据（假设格式为：温度,湿度,风速,气压）
                    values = [float(x) for x in data.split(',')]
                    sensor_data = {
                        'Temperature (°F)': values[0],
                        'Humidity (%)': values[1],
                        'Wind Speed (mph)': values[2],
                        'Pre': values[3]
                    }
                    
                    # 检查是否超过阈值
                    alerts = self.check_thresholds(sensor_data)
                    if alerts:
                        print("\n警告！以下参数超过阈值：")
                        for alert in alerts:
                            print(alert)
                        # 导航到安全屋
                        self.navigate_to_safe_house()
                    
                    return sensor_data
            return None
        except Exception as e:
            print(f"获取ESP32数据时出错: {str(e)}")
            return None

    def predict_flood_risk(self, data):
        """预测洪水风险"""
        try:
            # 准备数据
            features = ['Temperature (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pre']
            X = pd.DataFrame([data])[features]
            
            # 标准化数据
            X_scaled = self.scaler.transform(X)
            
            # 预测风险
            risk = self.model.predict(X_scaled)[0]
            
            # 风险等级
            if risk < 0.3:
                level = "低风险"
            elif risk < 0.6:
                level = "中风险"
            else:
                level = "高风险"
            
            return risk, level
        except Exception as e:
            print(f"预测洪水风险时出错: {str(e)}")
            return None, None

    def save_model(self, model_path):
        """保存模型和标准化器"""
        try:
            # 创建模型目录
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # 保存模型
            joblib.dump(self.model, model_path)
            
            # 保存标准化器
            scaler_path = os.path.join(os.path.dirname(model_path), 'scaler.joblib')
            joblib.dump(self.scaler, scaler_path)
            
            print(f"\n模型已保存到: {model_path}")
            print(f"标准化器已保存到: {scaler_path}")
            return True
        except Exception as e:
            print(f"保存模型时出错: {str(e)}")
            return False

def main():
    print("欢迎使用洪水预测系统")
    print("=" * 50)
    
    # 初始化预测器
    predictor = FloodPredictor()
    
    # 加载数据
    data_path = r"C:\Users\春阳面\Desktop\weather_data.xlsx"
    df = predictor.load_data(data_path)
    if df is None:
        return
    
    # 分析天气模式
    if not predictor.analyze_weather_patterns(df):
        return
    
    # 预处理数据
    X, y = predictor.preprocess_data(df)
    if X is None or y is None:
        return
    
    # 训练模型
    if predictor.train_model(X, y):
        # 保存模型
        model_path = "models/flood_prediction_model.joblib"
        predictor.save_model(model_path)
        
        print("\n模型训练完成！")
        print("分析结果已保存到 analysis_plots 目录。")
        
        # 连接ESP32
        if predictor.connect_esp32():
            print("\n开始实时监测...")
            while True:
                # 获取ESP32数据
                data = predictor.get_esp32_data()
                if data:
                    # 预测洪水风险
                    risk, level = predictor.predict_flood_risk(data)
                    if risk is not None:
                        print(f"\n当前洪水风险: {risk:.2f} ({level})")
                        print(f"温度: {data['Temperature (°F)']}°F")
                        print(f"湿度: {data['Humidity (%)']}%")
                        print(f"风速: {data['Wind Speed (mph)']} mph")
                        print(f"气压: {data['Pre']}")
                
                # 等待1秒
                time.sleep(1)
    else:
        print("\n模型训练失败，请检查数据格式是否正确。")

if __name__ == "__main__":
    main() 