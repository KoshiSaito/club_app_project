import streamlit as st

st.title('部活の情報アプリ')

# 練習メニュー
st.header('今日の練習メニュー')
st.text('ランニング、ストレッチ、技術練習')

# 天気情報
st.header('今日の天気')
st.text('晴れ')

# ブログ記事
st.header('ブログ記事のまとめ')
st.text('最新のブログ記事をここに表示')

st.radio("what is favorite part of triathlon?", ('bike', 'swim', 'run'))