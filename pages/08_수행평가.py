
import streamlit as st
import statistics

# ---------------------------------
# 페이지 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="지하철 혼잡도 분석",
    page_icon="🚇",
    layout="wide"
)

# ---------------------------------
# 제목
# ---------------------------------
st.title("🚇 지하철 혼잡도 분석 및 시간 추천")
st.write(
    "시간대별 지하철 혼잡도를 확인하고 "
    "비교적 여유로운 시간대를 추천받아 보세요!"
)

st.info(
    "현재 예시 데이터로 작동하는 프로그램입니다. "
    "실제 지하철 통계가 아닌 테스트용 수치입니다."
)

# ---------------------------------
# 예시 데이터
# 시간대: 06시 ~ 23시
# ---------------------------------
times = [
    "06시", "07시", "08시", "09시",
    "10시", "11시", "12시", "13시",
    "14시", "15시", "16시", "17시",
    "18시", "19시", "20시", "21시",
    "22시", "23시"
]

subway_data = {
    "2호선": {
        "강남역": {
            "평일": [25, 55, 95, 75, 50, 45, 50, 48, 45, 50, 65, 85, 100, 90, 70, 55, 40, 25],
            "주말": [15, 25, 40, 45, 55, 65, 75, 80, 85, 90, 85, 80, 75, 70, 65, 55, 40, 25]
        },
        "홍대입구역": {
            "평일": [20, 45, 80, 70, 50, 45, 50, 55, 60, 65, 75, 85, 90, 80, 65, 50, 35, 20],
            "주말": [15, 25, 35, 45, 60, 75, 85, 90, 95, 100, 95, 90, 85, 80, 70, 60, 45, 30]
        },
        "잠실역": {
            "평일": [20, 50, 90, 75, 55, 50, 55, 50, 50, 55, 70, 85, 95, 85, 65, 50, 35, 20],
            "주말": [15, 25, 40, 50, 65, 75, 85, 90, 95, 95, 90, 85, 80, 75, 65, 55, 40, 25]
        }
    },
    "3호선": {
        "연신내역": {
            "평일": [20, 50, 85, 70, 45, 40, 45, 45, 40, 45, 60, 80, 90, 75, 55, 40, 30, 20],
            "주말": [10, 20, 35, 45, 55, 65, 75, 80, 85, 90, 85, 80, 70, 65, 55, 45, 35, 20]
        },
        "고속터미널역": {
            "평일": [25, 55, 90, 75, 55, 50, 55, 55, 50, 55, 70, 85, 95, 85, 70, 55, 40, 25],
            "주말": [15, 25, 40, 50, 65, 75, 85, 90, 95, 100, 95, 90, 85, 75, 65, 55, 40, 25]
        }
    },
    "4호선": {
        "명동역": {
            "평일": [15, 40, 75, 65, 45, 40, 45, 50, 55, 60, 70, 80, 85, 75, 60, 45, 30, 15],
            "주말": [10, 20, 35, 45, 60, 75, 85, 90, 95, 100, 95, 90, 80, 75, 65, 55, 40, 25]
        },
        "서울역": {
            "평일": [30, 60, 95, 80, 55, 50, 55, 50, 45, 50, 65, 80, 95, 85, 65, 50, 35, 20],
            "주말": [20, 30, 45, 55, 65, 75, 80, 85, 90, 95, 90, 85, 80, 75, 65, 55, 40, 25]
        }
    }
}

# ---------------------------------
# 사용자 선택
# ---------------------------------
st.sidebar.header("🔎 분석 조건")

selected_line = st.sidebar.selectbox(
    "지하철 노선을 선택하세요",
    list(subway_data.keys())
)

station_list = list(subway_data[selected_line].keys())

selected_station = st.sidebar.selectbox(
    "역을 선택하세요",
    station_list
)

selected_day = st.sidebar.radio(
    "요일을 선택하세요",
    ["평일", "주말"]
)

# ---------------------------------
# 선택한 데이터 가져오기
# ---------------------------------
crowd = subway_data[selected_line][selected_station][selected_day]

average_crowd = statistics.mean(crowd)

# ---------------------------------
# 평균 혼잡도
# ---------------------------------
st.subheader("📊 선택한 역의 혼잡도")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("선택한 노선", selected_line)

with col2:
    st.metric("선택한 역", selected_station)

with col3:
    st.metric("평균 혼잡도", f"{average_crowd:.1f}점")

# ---------------------------------
# 시간대별 혼잡도 그래프
# ---------------------------------
st.subheader("📈 시간대별 지하철 혼잡도")

chart_data = {
    "혼잡도": crowd
}

st.bar_chart(chart_data)

st.caption("혼잡도 점수는 0~100의 예시 수치입니다.")

# ---------------------------------
# 가장 혼잡한 시간대 TOP 2
# ---------------------------------
st.subheader("🔥 가장 혼잡한 시간대 TOP 2")

ranked_crowd = sorted(
    zip(times, crowd),
    key=lambda item: item[1],
    reverse=True
)

for rank, (time, value) in enumerate(ranked_crowd[:2], start=1):
    st.write(f"**{rank}위: {time} — {value}점**")
    st.progress(value / 100)

# ---------------------------------
# 비교적 여유로운 시간대 TOP 2
# ---------------------------------
st.subheader("🌿 비교적 여유로운 시간대 TOP 2")

quiet_times = sorted(
    zip(times, crowd),
    key=lambda item: item[1]
)

for rank, (time, value) in enumerate(quiet_times[:2], start=1):
    st.write(f"**{rank}위: {time} — {value}점**")
    st.progress(value / 100)

st.success(
    f"추천 시간대는 {quiet_times[0][0]}과 "
    f"{quiet_times[1][0]}입니다. "
    "예시 데이터에서 혼잡도가 낮은 시간대입니다."
)

# ---------------------------------
# 다른 역과 평균 혼잡도 비교
# ---------------------------------
st.subheader("🚉 같은 노선의 역별 평균 혼잡도 비교")

station_averages = {}

for station, day_data in subway_data[selected_line].items():
    values = day_data[selected_day]
    station_averages[station] = statistics.mean(values)

comparison_data = {
    "평균 혼잡도": station_averages
}

st.bar_chart(comparison_data)

# ---------------------------------
# 분석 결과
# ---------------------------------
st.subheader("💡 분석 결과")

busiest_time, busiest_value = ranked_crowd[0]
quietest_time, quietest_value = quiet_times[0]

st.write(
    f"- 선택한 역의 평균 혼잡도는 **{average_crowd:.1f}점**입니다."
)

st.write(
    f"- 가장 혼잡한 시간대는 **{busiest_time}**이며 "
    f"혼잡도는 **{busiest_value}점**입니다."
)

st.write(
    f"- 가장 여유로운 시간대는 **{quietest_time}**이며 "
    f"혼잡도는 **{quietest_value}점**입니다."
)

st.divider()

st.caption(
    "※ 본 프로그램은 파이썬의 statistics와 Streamlit 기본 그래프 기능을 사용합니다. "
    "실제 이용 시에는 실제 지하철 혼잡도 데이터를 연결해야 합니다."
)
