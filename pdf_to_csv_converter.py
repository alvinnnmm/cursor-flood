import pdfplumber
import pandas as pd
import os
from datetime import datetime
import re

def extract_kuching_weather(pdf_path):
    """
    从PDF文件中提取古晋天气数据
    :param pdf_path: PDF文件路径
    :return: 包含天气数据的DataFrame
    """
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取文本
            text = page.extract_text()
            if text:
                print(f"\nProcessing page text:\n{text[:500]}...")
                
                # 按行分割文本
                lines = text.split('\n')
                
                # 查找包含天气数据的行
                for i, line in enumerate(lines):
                    # 检查是否包含日期格式
                    if re.search(r'\d{1,2}/\d{1,2}/\d{4}', line):
                        # 提取日期
                        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', line)
                        if date_match:
                            date = date_match.group(1)
                            
                            # 提取数值
                            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                            
                            if len(numbers) >= 3:
                                data.append({
                                    'date': date,
                                    'temperature': float(numbers[0]),
                                    'humidity': float(numbers[1]),
                                    'rainfall': float(numbers[2])
                                })
                                print(f"Found data: {date}, {numbers}")
    
    return pd.DataFrame(data)

def extract_flood_data(text):
    """
    从文本中提取洪水数据
    :param text: 包含洪水数据的文本
    :return: 包含洪水数据的DataFrame
    """
    data = []
    
    # 分割成单独的事件
    events = re.split(r'\n\n', text.strip())
    
    for event in events:
        if not event.strip():
            continue
            
        try:
            # 提取日期和时间
            date_time_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}[ap]m)\s*-\s*(\d{2}:\d{2}[ap]m)', event)
            if not date_time_match:
                continue
                
            date = date_time_match.group(1)
            start_time = date_time_match.group(2)
            end_time = date_time_match.group(3)
            
            # 提取地点
            location_match = re.search(r'地点：(.+?)(?=\n|$)', event)
            location = location_match.group(1) if location_match else None
            
            # 提取洪水高度
            height_match = re.search(r'洪水高度：(.+?)(?=\n|$)', event)
            height = height_match.group(1) if height_match else None
            
            # 提取原因
            cause_match = re.search(r'原因：(.+?)(?=\n|$)', event)
            cause = cause_match.group(1) if cause_match else None
            
            data.append({
                'date': date,
                'start_time': start_time,
                'end_time': end_time,
                'location': location,
                'height': height,
                'cause': cause
            })
            
        except Exception as e:
            print(f"Error processing event: {str(e)}")
            print(f"Event text: {event}")
    
    return pd.DataFrame(data)

def convert_pdfs_to_csv(pdf_dir, output_dir):
    """
    将目录中的所有PDF文件转换为CSV格式
    :param pdf_dir: PDF文件目录
    :param output_dir: 输出目录
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 处理每个月的天气数据
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf') and 'Weather History' in filename:
            pdf_path = os.path.join(pdf_dir, filename)
            try:
                print(f"\nProcessing file: {filename}")
                df = extract_kuching_weather(pdf_path)
                
                if not df.empty:
                    # 保存为CSV
                    output_path = os.path.join(output_dir, f"kuching_weather_{filename.split('_')[-1].replace('.pdf', '.csv')}")
                    df.to_csv(output_path, index=False)
                    print(f"Saved to: {os.path.basename(output_path)}")
                    print(f"Data shape: {df.shape}")
                    print("First few rows:")
                    print(df.head())
                else:
                    print(f"No data extracted from {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def main():
    # 设置输入和输出目录
    pdf_dir = "Flood data"
    output_dir = "converted_data"
    
    print("Starting PDF conversion...")
    convert_pdfs_to_csv(pdf_dir, output_dir)
    print("Conversion completed!")

    # 洪水数据文本
    flood_text = """
    03/01/2023 11:00am - 04:00pm：
    地点：Kuching, SK Matang
    洪水高度：0.5m
    原因：持续的强降雨和排水系统不足导致水流溢出到低洼地区​。

    25/01/2023 07:00am - 11:00am：
    地点：Lundu, Kuching, SK Jangkar
    洪水高度：0.1m - 0.4m
    原因：持续降雨导致Sungai Jangkar水位上涨并溢出​。

    29/01/2023 03:00am - 08:00am：
    地点：Kuching, Jalan Quop 和 Jalan Saput
    洪水高度：0.15m - 0.35m
    原因：持续降雨和排水系统无法容纳积水，导致低洼区域积水​。

    29/01/2023 09:00am - 03:00pm：
    地点：Bau, Kampung Jugan
    洪水高度：0.6m
    原因：持续降雨导致Sungai Mutut水位上升并溢出​。

    29/01/2023 09:00am - 03:00pm：
    地点：Bau, Kampung Bobak
    洪水高度：0.6m
    原因：降雨导致Sungai Bubut和Sungai Tombom水位上涨并溢出​。

    29/01/2023 05:00pm - 11:00pm：
    地点：Bau, Kampung Bogag
    洪水高度：0.1m
    原因：持续降雨导致Sungai Noren水位上涨并溢出​。

    01/03/2023 07:30am - 07:00pm：
    地点：Kuching, Kampung Keranji
    洪水高度：0.6m - 0.7m
    原因：持续降雨和Sungai Sarawak及其他支流水位上涨导致低洼地区被淹​。

    03/03/2023 06:00pm - 09:00pm：
    地点：Kuching, Kampung Matang
    洪水高度：0.3m - 0.45m
    原因：暴雨导致Sungai Cina水位上涨，溢出到附近低洼地区​。

    04/03/2023 07:00pm - 09:00pm：
    地点：Kuching, Kampung Judin
    洪水高度：0.3m - 0.6m
    原因：持续降雨和Sungai Sebako水位上涨​。

    09/03/2023 05:30am - 08:00am：
    地点：Lundu, Kuching, Kampung Judin
    洪水高度：0.3m - 0.6m
    原因：持续降雨和Sungai Sebako溢出​。
    """
    
    # 提取洪水数据
    flood_df = extract_flood_data(flood_text)
    
    if not flood_df.empty:
        # 保存为CSV
        output_path = os.path.join(output_dir, "kuching_flood_events_2023.csv")
        flood_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved flood data to: {os.path.basename(output_path)}")
        print(f"Data shape: {flood_df.shape}")
        print("\nFirst few rows:")
        print(flood_df.head())
    else:
        print("No flood data extracted")

if __name__ == "__main__":
    main() 