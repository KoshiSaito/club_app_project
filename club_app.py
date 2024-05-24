import streamlit as st
import weather_functions as wf

# Streamlitのセッション状態を取得
session_state = st.session_state

# セッション状態が初期化されていない場合は初期化する
if 'current_weather_info' not in session_state:
    session_state.current_weather_info = None

if 'tomorrow_weather_info' not in session_state:
    session_state.tomorrow_weather_info = None

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

# 現在の天気情報を表示する領域
st.header("現在の天気情報")
if st.button("現在の天気情報を取得する",key=1):
    if location:
        latitude = locations[location]["lat"]
        longitude = locations[location]["lon"]
        current_weather_info = wf.get_current_weather_info(latitude, longitude, openweathermap_api_key)
        if isinstance(current_weather_info, dict):
            session_state.current_weather_info = current_weather_info
            for key, value in session_state.current_weather_info.items():
                st.write(f"{key}: {value}")
            google_map_url = wf.generate_google_map_url(latitude, longitude)
            st.write(f"Google Map URL: {google_map_url}")
        else:
            st.error("天気情報の取得に失敗しました。")
    else:
        st.warning("地域を選択してください。")

# n時間後の天気情報を表示する領域
st.header("n時間後の天気情報")
hours_ahead = st.slider("何時間後の天気情報を取得しますか？", 0, 24, 0, step=3)
if st.button(f"{hours_ahead}時間後の天気情報を取得する",key=2):
    if location:
        latitude = locations[location]["lat"]
        longitude = locations[location]["lon"]
        tomorrow_weather_info = wf.get_tomorrow_weather_info(latitude, longitude, openweathermap_api_key, hours_ahead)
        if isinstance(tomorrow_weather_info, dict):
            session_state.tomorrow_weather_info = tomorrow_weather_info
            for key, value in session_state.tomorrow_weather_info.items():
                st.write(f"{key}: {value}")
            google_map_url = wf.generate_google_map_url(latitude, longitude)
            st.write(f"Google Map URL: {google_map_url}")
        else:
            st.error("天気情報の取得に失敗しました。")
    else:
        st.warning("地域を選択してください。")