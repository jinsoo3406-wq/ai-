import pandas as pd
import pydeck as pdk
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="서울 외국인 관광 명소 TOP 10",
    page_icon="🗺️",
    layout="wide",
)

# 타이틀 및 설명
st.title("🇰🇷 외국인 관광객이 가장 사랑하는 서울 핫플 TOP 10")
st.markdown(
    "스트림릿(Streamlit)과 Pydeck 지도를 활용해 외국인들이 꼭 찾는 서울의 대표 관광지 10곳을 지도에 표시했습니다."
)

# 외국인 선호 서울 관광지 TOP 10 데이터 (내장 데이터)
data = {
    "장소": [
        "경복궁",
        "명동 쇼핑거리",
        "N서울타워 (남산)",
        "북촌한옥마을",
        "동대문디자인플라자(DDP)",
        "홍대 (홍익대 거리)",
        "잠실 롯데월드 & 타워",
        "광장시장",
        "국립중앙박물관",
        "반포 한강공원",
    ],
    "설명": [
        "조선시대의 대표 궁궐이자 한복 체험 명소",
        "K-뷰티, 쇼핑, 길거리 음식을 즐기는 쇼핑 1번지",
        "서울의 전경과 야경을 한눈에 담는 랜드마크",
        "한국 전통 가옥(한옥)의 아름다움을 느낄 수 있는 마을",
        "세계적인 건축가 자하 하디드가 설계한 복합문화공간",
        "젊음의 거리, 버스킹과 트렌디한 클럽/카페 문화",
        "초고층 전망대(서울스카이)와 대형 테마파크",
        "빈대떡, 마약김밥 등 전통 시장의 맛을 느끼는 곳",
        "한국의 역사와 유물을 한눈에 볼 수 있는 최고 박물관",
        "한강 라면과 야경, 치맥을 즐길 수 있는 시민들의 휴식처",
    ],
    "lat": [
        37.5796,
        37.5636,
        37.5512,
        37.5826,
        37.5665,
        37.5563,
        37.5133,
        37.5700,
        37.5239,
        37.5110,
    ],
    "lon": [
        126.9770,
        126.9822,
        126.9882,
        126.9838,
        126.9909,
        126.9227,
        127.1001,
        126.9994,
        126.9797,
        126.9918,
    ],
}

df = pd.DataFrame(data)

# 사이드바 설정 (관광지 목록 확인용)
st.sidebar.header("📍 관광지 목록 보기")
selected_spot = st.sidebar.selectbox("원하는 장소를 선택하세요:", df["장소"])

# 선택된 장소의 정보 필터링
spot_info = df[df["장소"] == selected_spot].iloc[0]

# 레이아웃 구성 (좌측: 지도, 우측: 상세 정보)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ 서울 관광지도 (Pydeck)")

    # Pydeck을 이용한 3D 인터랙티브 지도 구현
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 75, 75, 200],  # 포인트 색상 (빨간색 계열)
        get_radius=300,  # 원 크기
        pickable=True,
        auto_highlight=True,
    )

    # 서울 중심부 초기 좌표 설정
    view_state = pdk.ViewState(
        latitude=37.555, longitude=126.975, zoom=11, pitch=30
    )

    # 툴팁 설정
    tooltip = {
        "html": "<b>장소:</b> {장소}<br/><b>설명:</b> {설명}",
        "style": {
            "background": "grey",
            "color": "white",
            "font-family": "sans-serif",
            "z-index": "10000",
        },
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(r)

with col2:
    st.subheader("💡 선택된 핫플 정보")
    st.markdown(f"### **{spot_info['장소']}**")
    st.info(spot_info["설명"])
    st.write(f"📌 **위도:** {spot_info['lat']}")
    st.write(f"📌 **경도:** {spot_info['lon']}")

    st.markdown("---")
    st.markdown("### 📋 전체 TOP 10 리스트")
    for idx, row in df.iterrows():
        st.write(f"**{idx+1}. {row['장소']}**")

# 하단 데이터 테이블 표시
with st.expander("📊 전체 데이터 테이블 보기"):
    st.dataframe(df[["장소", "설명", "lat", "lon"]])
