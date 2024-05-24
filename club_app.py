import streamlit as st
import requests
from datetime import datetime, timedelta
import os

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

        # タイムスタンプを日本標準時 (JST) に変換
        utc_timestamp = datetime.fromtimestamp(data['dt'])
        jst_timestamp = utc_timestamp + timedelta(hours=9)
        current_timestamp = jst_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "Current Weather": current_weather,
            "Current Temperature": f"{current_temperature} ℃",
            "Current Wind Speed": f"{current_wind_speed} m/s",
            "Current Wind Direction": current_wind_direction,
            "Current Timestamp": current_timestamp
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

# 地域名と緯度・経度の対応辞書
locations = {
    "東京": {"lat": 35.682839, "lon": 139.759455},
    "大阪": {"lat": 34.693737, "lon": 135.502167},
    "名古屋": {"lat": 35.181446, "lon": 136.906398},
    "福岡": {"lat": 33.590355, "lon": 130.401716},
    "札幌": {"lat": 43.062096, "lon": 141.354376},
    "海づり公園": {"lat": 33.627800, "lon": 130.227800},
    "松原北": {"lat": 33.578277, "lon": 130.144815},
    "地球": {"lat": 0, "lon": 0}
}

# streamlitアプリケーションの設定
st.title("天気情報アプリ")

# 地域の選択
location = st.selectbox("地域を選択してください", list(locations.keys()))

# APIキーの取得
openweathermap_api_key = st.secrets['club']["API_KEY"]

# 天気情報の取得と表示
if st.button("天気情報を取得する"):
    if location:
        latitude = locations[location]["lat"]
        longitude = locations[location]["lon"]
        current_weather_info = get_current_weather_info(latitude, longitude, openweathermap_api_key)
        if isinstance(current_weather_info, dict):
            st.write(f"{location}の現在の気象情報:")
            for key, value in current_weather_info.items():
                st.write(f"{key}: {value}")
            google_map_url = generate_google_map_url(latitude, longitude)
            st.write(f"Google Map URL: {google_map_url}")
        else:
            st.error("天気情報の取得に失敗しました。")
    else:
        st.warning("地域を選択してください。")

# n時間後の天気情報の取得と表示 0時間後の天気情報は現在の天気情報と同じ
hours_ahead = st.slider("何時間後の天気情報を取得しますか？", 0, 24, 0, step=3) # 引数: (ラベル, 最小値, 最大値, 初期値)
if st.button(f"{hours_ahead}時間後の天気情報を取得する"):
    if location:
        latitude = locations[location]["lat"]
        longitude = locations[location]["lon"]
        tomorrow_weather_info = get_tomorrow_weather_info(latitude, longitude, openweathermap_api_key, hours_ahead)
        if isinstance(tomorrow_weather_info, dict):
            st.write(f"{location}の{hours_ahead}時間後の気象情報:")
            for key, value in tomorrow_weather_info.items():
                st.write(f"{key}: {value}")
            google_map_url = generate_google_map_url(latitude, longitude)
            st.write(f"Google Map URL: {google_map_url}")
        else:
            st.error("天気情報の取得に失敗しました。")
    else:
        st.warning("地域を選択してください。")