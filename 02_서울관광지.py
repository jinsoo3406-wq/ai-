Python
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 외국인 관광 명소 TOP 10 (Folium)",
    page_icon="🗺️",
    layout="wide",
)

# 타이틀 및 설명
st.title("🇰🇷 외국인 관광객이 가장 사랑하는 서울 핫플 TOP 10")
st.markdown(
    "스트림릿(Streamlit)과 **Folium** 지도를 활용해 외국인들이 꼭 찾는 서울의 대표 관광지 10곳을 지도에 표시했습니다."
)

# 외국인 선호 서울 관광지 TOP 10 데이터
data = {
    "
