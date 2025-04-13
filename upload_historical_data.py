import requests
import json
from datetime import datetime
import time
import sys

# 配置
BASE_URL = "http://127.0.0.1:5000"  # 使用本地地址
USERNAME = "yapa920@gmail.com"
PASSWORD = "Alvin1234567"

# 砂拉越历史洪水数据
HISTORICAL_DATA = [
    # 1985-1989年的记录
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1985-01-01",
        "river_level": None,
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Sg.Sarawak, Kuching Town",
        "comments": "Flash Flood"
    },
    {
        "location": {"latitude": 4.0000, "longitude": 113.9000},  # Btg Tatau位置
        "date": "1985-05-01",
        "river_level": 1.8,  # 6英尺转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Btg. Tatau & Batang Kemena",
        "comments": ""
    },
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1986-03-01",
        "river_level": None,
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Kuching Town",
        "comments": ""
    },
    {
        "location": {"latitude": 2.3000, "longitude": 111.8300},  # 诗巫位置
        "date": "1988-01-01",
        "river_level": None,
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Sibu Town",
        "comments": ""
    },
    {
        "location": {"latitude": 2.3000, "longitude": 111.8300},  # 诗巫位置
        "date": "1988-08-01",
        "river_level": 0.76,  # 2.5英尺转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Kanowit, Balingian areas",
        "comments": ""
    },
    # 1990-1996年的记录
    {
        "location": {"latitude": 2.3000, "longitude": 111.8300},  # 诗巫位置
        "date": "1991-02-01",
        "river_level": 0.45,  # 0.3-0.6米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Sg.Igan, Batang Rajang",
        "comments": ""
    },
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1992-01-01",
        "river_level": 1.83,  # 6英尺转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Sg.Sarawak, Lundu Area",
        "comments": ""
    },
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1993-12-01",
        "river_level": 0.3,  # 1-8英尺的平均值转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Kuching, Lundu, Sibu Town, Dalat, Mukah, Matu/Julau dan Limbang",
        "comments": ""
    },
    {
        "location": {"latitude": 2.3000, "longitude": 111.8300},  # 诗巫位置
        "date": "1994-02-01",
        "river_level": 3.05,  # 10英尺转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Belaga, Kapit etc",
        "comments": "severe flooding at upper Batang Rajang"
    },
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1995-02-01",
        "river_level": 1.52,  # 5英尺转换为米
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Sg.Sarawak and Kuching Town (Batu Kitang shophouses)",
        "comments": ""
    },
    {
        "location": {"latitude": 1.5600, "longitude": 110.3400},  # 古晋位置
        "date": "1996-02-01",
        "river_level": 0.95,  # 0.1m-1.8m的平均值
        "flood_occurred": True,
        "weather_conditions": {},
        "affected_areas": "Coastal area of Kuching Division, Lower Rajang, Lower Baram and Lower Limbang",
        "comments": "duration from few hours to 3 weeks"
    }
]

def print_progress(current, total):
    """显示上传进度"""
    progress = (current / total) * 100
    sys.stdout.write(f"\r上传进度: {current}/{total} ({progress:.1f}%)")
    sys.stdout.flush()

def login():
    """登录系统并获取访问令牌"""
    print("正在登录系统...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        response.raise_for_status()
        print("登录成功！")
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"\n登录失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"错误详情: {e.response.text}")
        return None

def upload_flood_record(token, record, current, total):
    """上传单个洪水记录"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/history/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=record
        )
        response.raise_for_status()
        print_progress(current, total)
        return True
    except requests.exceptions.RequestException as e:
        print(f"\n上传记录失败 {record['date']}: {e}")
        if hasattr(e.response, 'text'):
            print(f"错误详情: {e.response.text}")
        return False

def main():
    print("开始上传砂拉越历史洪水数据...")
    print(f"总记录数: {len(HISTORICAL_DATA)}")
    
    # 登录获取令牌
    token = login()
    if not token:
        print("无法获取访问令牌，程序退出")
        return

    # 上传所有记录
    success_count = 0
    total_records = len(HISTORICAL_DATA)
    
    for i, record in enumerate(HISTORICAL_DATA, 1):
        if upload_flood_record(token, record, i, total_records):
            success_count += 1
        time.sleep(0.5)  # 添加延迟以避免请求过快

    print(f"\n\n上传完成！")
    print(f"总记录数: {total_records}")
    print(f"成功上传: {success_count}")
    print(f"失败: {total_records - success_count}")

if __name__ == "__main__":
    main() 