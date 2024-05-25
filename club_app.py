import streamlit as st
import weather_functions as wf

# Streamlitのセッション状態を取得
session_state = st.session_state

# セッション状態が初期化されていない場合は初期化する
if 'current_weather_info' not in session_state:
    session_state.current_weather_info = {}
if 'tomorrow_weather_info' not in session_state:
    session_state.tomorrow_weather_info = {}
if 'selected_location' not in session_state:
    session_state.selected_location = None

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
selected_location = st.selectbox("地域を選択してください", list(locations.keys()), key='location_select')

# APIキーの取得
openweathermap_api_key = st.secrets['club']["API_KEY"]

# 地域選択が変わったらセッション状態を更新
if selected_location != session_state.selected_location:
    session_state.selected_location = selected_location

# 現在の天気情報を表示する領域
st.header("現在の天気情報")
if st.button("現在の天気情報を取得する", key=1):
    if session_state.selected_location:
        latitude = locations[session_state.selected_location]["lat"]
        longitude = locations[session_state.selected_location]["lon"]
        current_weather_info = wf.get_current_weather_info(latitude, longitude, openweathermap_api_key)
        if isinstance(current_weather_info, dict):
            session_state.current_weather_info[session_state.selected_location] = current_weather_info
            for key, value in session_state.current_weather_info[session_state.selected_location].items():
                st.write(f"{key}: {value}")
            # iconの表示
            st.image(session_state.current_weather_info[session_state.selected_location]["Current Weather Icon"], width=100)
            # google mapの埋め込み
            st.write(f"Google Map: [Link]({wf.generate_google_map_url(latitude, longitude)})")
        else:
            st.error("天気情報の取得に失敗しました。")

# n時間後の天気情報を表示する領域
st.header("n時間後の天気情報")
hours_ahead = st.slider("何時間後の天気情報を取得しますか？", 0, 24, 0, step=3)  # 引数：(ラベル, 最小値, 最大値, 初期値, ステップ)
# n時間後の天気情報を取得するボタン ボタンの表示は入力によって変わる
if st.button(f"{hours_ahead}時間後の天気情報を取得する"):
    if session_state.selected_location:
        latitude = locations[session_state.selected_location]["lat"]
        longitude = locations[session_state.selected_location]["lon"]
        tomorrow_weather_info = wf.get_tomorrow_weather_info(latitude, longitude, openweathermap_api_key, hours_ahead)
        if isinstance(tomorrow_weather_info, dict):
            session_state.tomorrow_weather_info[session_state.selected_location] = tomorrow_weather_info
            for key, value in session_state.tomorrow_weather_info[session_state.selected_location].items():
                st.write(f"{key}: {value}")
            # google mapの埋め込み
            st.write(f"Google Map: [Link]({wf.generate_google_map_url(latitude, longitude)})")  # リンクを表示
        else:
            st.error("天気情報の取得に失敗しました。")
