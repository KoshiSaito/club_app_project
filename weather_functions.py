import requests
from datetime import datetime, timedelta
import random
import streamlit as st
import matplotlib.pyplot as plt


# 関数定義
def convert_wind_direction(deg):
    directions = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東", "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西"]
    index = round((deg % 360) / 22.5)
    return directions[index % 16]

def get_current_weather_info(latitude, longitude, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        current_weather = data['weather'][0]['description']
        current_temperature = data['main']['temp']
        current_wind_speed = data['wind']['speed']
        current_wind_direction = convert_wind_direction(data['wind']['deg'])
        current_weather_icon = data['weather'][0]['icon'] # アイコンのID

        # タイムスタンプを日本標準時 (JST) に変換
        utc_timestamp = datetime.fromtimestamp(data['dt'])
        jst_timestamp = utc_timestamp + timedelta(hours=9)
        current_timestamp = jst_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "Current Weather": current_weather,
            "Current Temperature": f"{current_temperature} ℃",
            "Current Wind Speed": f"{current_wind_speed} m/s",
            "Current Wind Direction": current_wind_direction,
            "Current Timestamp": current_timestamp,
            "Current Weather Icon": f"http://openweathermap.org/img/w/{current_weather_icon}.png" # アイコンのURL
        }
    else:
        return "Failed to retrieve current weather information."
    
def get_tomorrow_weather_info(latitude, longitude, api_key, hours_ahead):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # OpenWeatherMapの予報は3時間ごとのため、hours_aheadを3で割ってインデックスを計算
        index = hours_ahead // 3 # 3時間ごとの予報
        if index < len(data['list']):
            forecast = data['list'][index]
            weather = forecast['weather'][0]['description']
            temperature = forecast['main']['temp']
            wind_speed = forecast['wind']['speed']
            wind_direction = convert_wind_direction(forecast['wind']['deg'])
            # タイムスタンプを日本標準時 (JST) に変換
            utc_timestamp = datetime.fromtimestamp(forecast['dt'])
            jst_timestamp = utc_timestamp + timedelta(hours=9)
            tomorrow_timestamp = jst_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            return {
                "Tomorrow Weather": weather,
                "Tomorrow Temperature": f"{temperature} ℃",
                "Tomorrow Wind Speed": f"{wind_speed} m/s",
                "Tomorrow Wind Direction": wind_direction,
                "Tomorrow Timestamp": tomorrow_timestamp
            }
        else:
            return "Failed to retrieve weather information."
    else:
        return "Failed to retrieve weather information."
    
def generate_google_map_url(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

def get_fortune():
    fortunes = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
    return f"今日の運勢: {fortunes[random.randint(0, len(fortunes)-1)]}"

def visualize_weather_info(latitude, longitude, api_key):
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        daily_weather = data['daily']
        dates = []
        max_temps = []
        min_temps = []
        weather_icons = []
        for day in daily_weather:
            dates.append(datetime.fromtimestamp(day['dt']).strftime('%m/%d'))
            max_temps.append(day['temp']['max'])
            min_temps.append(day['temp']['min'])
            weather_icons.append(f"http://openweathermap.org/img/w/{day['weather'][0]['icon']}.png")
        # グラフの描画
        fig, ax = plt.subplots()
        ax.plot(dates, max_temps, label='最高気温', marker='o')
        ax.plot(dates, min_temps, label='最低気温', marker='o')
        ax.set_xlabel('日付')
        ax.set_ylabel('気温 (℃)')
        ax.set_title('天気予報')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("weather_info.png")
    else:
        st.error("Failed to retrieve weather information.")