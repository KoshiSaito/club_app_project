import streamlit as st
import requests
from datetime import datetime
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
        current_timestamp = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "Current Weather": current_weather,
            "Current Temperature": f"{current_temperature} ℃",
            "Current Wind Speed": f"{current_wind_speed} m/s",
            "Current Wind Direction": current_wind_direction,
            "Current Timestamp": current_timestamp
        }
    else:
        return "Failed to retrieve current weather information."

def generate_google_map_url(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

# streamlitアプリケーションの設定
st.title("天気情報アプリ")

# 緯度と経度の入力フォーム
latitude = st.text_input("緯度を入力してください")
longitude = st.text_input("経度を入力してください")

# APIキーの取得
openweathermap_api_key = st.secrets["API_KEY"]

# 天気情報の取得と表示
if st.button("天気情報を取得する"):
    if latitude and longitude:
        current_weather_info = get_current_weather_info(latitude, longitude, openweathermap_api_key)
        if isinstance(current_weather_info, dict):
            st.write("現在の気象情報:")
            for key, value in current_weather_info.items():
                st.write(f"{key}: {value}")
            google_map_url = generate_google_map_url(latitude, longitude)
            st.write(f"Google Map URL: {google_map_url}")
        else:
            st.error("天気情報の取得に失敗しました。")
    else:
        st.warning("緯度と経度を入力してください。")