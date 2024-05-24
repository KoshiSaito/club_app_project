import streamlit as st
import weather_functions as wf

# Streamlitのセッション状態を取得
session_state = st.session_state

# セッション状態が初期化されていない場合は初期化する
if 'current_weather_info' not in session_state:
    session_state.current_weather_info = {}
if 'tomorrow_weather_info' not in session_state:
    session_state.tomorrow_weather_info = {}
if 'count1' not in st.session_state: 
	st.session_state.count1 = 0 #countがsession_stateに追加されていない場合，0で初期化
if 'count2' not in st.session_state: 
	st.session_state.count2 = 0 #countがsession_stateに追加されていない場合，0で初期化

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
selected_location = st.selectbox("地域を選択してください", list(locations.keys()))

# APIキーの取得
openweathermap_api_key = st.secrets['club']["API_KEY"]

# 現在の天気情報を表示する領域
st.header("現在の天気情報")
if st.button("現在の天気情報を取得する", key=1) or st.session_state.count1 == 1:
    st.session_state.count1 = 1
    if selected_location:
        latitude = locations[selected_location]["lat"]
        longitude = locations[selected_location]["lon"]
        current_weather_info = wf.get_current_weather_info(latitude, longitude, openweathermap_api_key)
        if isinstance(current_weather_info, dict):
            session_state.current_weather_info[selected_location] = current_weather_info
            for key, value in session_state.current_weather_info[selected_location].items():
                st.write(f"{key}: {value}")
        else:
            st.error("天気情報の取得に失敗しました。")

# n時間後の天気情報を表示する領域
st.header("n時間後の天気情報")
hours_ahead = st.slider("何時間後の天気情報を取得しますか？", 1, 24, 3)
if st.button("n時間後の天気情報を取得する", key=2) or st.session_state.count2 == 1:
    st.session_state.count2 = 1
    if selected_location:
        latitude = locations[selected_location]["lat"]
        longitude = locations[selected_location]["lon"]
        tomorrow_weather_info = wf.get_tomorrow_weather_info(latitude, longitude, openweathermap_api_key, hours_ahead)
        if isinstance(tomorrow_weather_info, dict):
            session_state.tomorrow_weather_info[selected_location] = tomorrow_weather_info
            for key, value in session_state.tomorrow_weather_info[selected_location].items():
                st.write(f"{key}: {value}")
        else:
            st.error("天気情報の取得に失敗しました。")