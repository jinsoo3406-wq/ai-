
import streamlit as st
import statistics

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="지하철 혼잡도 분석",
    page_icon="🚇",
    layout="wide"
)

# -----------------------------------
# 제목
# -----------------------------------
st.title("🚇 지하철 혼잡도 분석 및 최적 시간 추천")
st.write("지하철 이용 데이터를 분석하고 덜 혼잡한 시간대를 찾아보세요!")
st.caption("현재 제공되는 데이터는 프로그램 테스트용 가상 데이터입니다.")

st.divider()

# -----------------------------------
# 가상 데이터
# 실제 지하철 혼잡도 통계가 아닙니다.
# -----------------------------------
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
            "평일": [35, 65, 95, 80, 55, 50, 45, 48, 50, 55, 65, 80, 98, 90, 75, 60, 45, 30],
            "주말": [20, 25, 35, 45, 55, 65, 70, 75, 80, 85, 90, 85, 80, 75, 65, 55, 40, 25]
        },
        "홍대입구역": {
            "평일": [30, 55, 80, 75, 60, 55, 50, 55, 60, 65, 75, 85, 90, 80, 70, 55, 40, 25],
            "주말": [15, 20, 30, 45, 60, 75, 85, 90, 95, 90, 85, 80, 75, 70, 60, 50, 35, 20]
        },
        "잠실역": {
            "평일": [25, 50, 85, 75, 55, 50, 45, 50, 55, 60, 70, 85, 95, 85, 70, 55, 40, 25],
            "주말": [20, 25, 35, 50, 65, 75, 85, 90, 95, 90, 85, 80, 75, 65, 50, 40, 30, 20]
        }
    },
    "3호선": {
        "교대역": {
            "평일": [25, 50, 90, 75, 55, 45, 40, 45, 50, 55, 65, 80, 95, 80, 65, 50, 35, 20],
            "주말": [15, 20, 30, 40, 50, 60, 70, 75, 80, 85, 80, 75, 70, 60, 45, 35, 25, 15]
        },
        "고속터미널역": {
            "평일": [30, 55, 85, 75, 60, 55, 50, 50, 55, 60, 70, 85, 95, 85, 70, 55, 40, 25],
            "주말": [20, 25, 35, 50, 65, 80, 90, 95, 90, 85, 80, 75, 70, 60, 50, 40, 30, 20]
        }
    },
    "4호선": {
        "명동역": {
            "평일": [20, 40, 65, 70, 65, 60, 55, 60, 65, 70, 75, 80, 85, 75, 60, 45, 30, 20],
            "주말": [15, 20, 30, 45, 60, 75, 85, 90, 95, 90, 85, 80, 75, 65, 50, 40, 30, 20]
        },
        "서울역": {
            "평일": [40, 70, 95, 85, 65, 55, 50, 55, 60, 65, 75, 85, 95, 90, 75, 60, 45, 30],
            "주말": [25, 35, 50, 60, 70, 75, 80, 85, 90, 85, 80, 75, 70, 60, 50, 40, 30, 20]
        }
    }
}

# -----------------------------------
# 사이드바: 분석 조건 선택
# -----------------------------------
st.sidebar.header("⚙️ 분석 조건")

line = st.sidebar.selectbox(
    "지하철 노선을 선택하세요",
    list(subway_data.keys())
)

station = st.sidebar.selectbox(
    "지하철역을 선택하세요",
    list(subway_data[line].keys())
)

day = st.sidebar.radio(
    "요일을 선택하세요",
    ["평일", "주말"]
)

# -----------------------------------
# 선택한 데이터 불러오기
# -----------------------------------
values = subway_data[line][station][day]

# -----------------------------------
# 혼잡도 계산 함수
# -----------------------------------
def get_level(value):
    if value >= 80:
        return "매우 혼잡 🔴"
    elif value >= 60:
        return "혼잡 🟠"
    elif value >= 40:
        return "보통 🟡"
    else:
        return "여유 🟢"

# -----------------------------------
# 선택 조건 표시
# -----------------------------------
st.subheader("📍 선택한 분석 조건")
st.write(f"**노선:** {line}")
st.write(f"**역:** {station}")
st.write(f"**요일:** {day}")

st.divider()

# -----------------------------------
# 주요 분석 결과
# -----------------------------------
average = statistics.mean(values)

sorted_indices = sorted(
    range(len(values)),
    key=lambda i: values[i],
    reverse=True
)

busy_indices = sorted_indices[:2]
quiet_indices = sorted_indices[-2:]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 평균 혼잡도", f"{average:.1f}%")

with col2:
    st.metric("🔥 가장 혼잡한 시간", times[busy_indices[0]])

with col3:
    st.metric("🌿 가장 여유로운 시간", times[quiet_indices[0]])

st.divider()

# -----------------------------------
# 시간대별 혼잡도 그래프
# -----------------------------------
st.subheader("📈 시간대별 혼잡도")

chart_data = {}

for i in range(len(times)):
    chart_data[times[i]] = values[i]

st.bar_chart(chart_data)

st.caption("혼잡도 수치는 프로그램 테스트용으로 만든 가상 수치입니다.")

# -----------------------------------
# 시간대별 상세 분석
# -----------------------------------
st.subheader("🕒 시간대별 혼잡도 상세 분석")

for i in range(len(times)):
    st.write(
        f"**{times[i]}** : {values[i]}%  |  {get_level(values[i])}"
    )
    st.progress(values[i] / 100)

st.divider()

# -----------------------------------
# 혼잡 시간 분석
# -----------------------------------
st.subheader("🔥 가장 혼잡한 시간대 TOP 2")

for rank, index in enumerate(busy_indices, start=1):
    st.write(
        f"{rank}위. **{times[index]}** - 혼잡도 {values[index]}%"
    )

st.divider()

# -----------------------------------
# 최적 시간 추천
# -----------------------------------
st.subheader("🌿 추천 이용 시간 TOP 2")

for rank, index in enumerate(quiet_indices, start=1):
    st.success(
        f"{rank}위. {times[index]} - 혼잡도 {values[index]}%"
    )

st.info(
    f"💡 {station}은(는) {times[quiet_indices[0]]}에 "
    "이용하면 선택한 조건 중 상대적으로 덜 혼잡할 것으로 예상돼요!"
)

st.divider()

# -----------------------------------
# 여러 역 비교
# -----------------------------------
st.subheader("🔍 지하철역별 혼잡도 비교")

stations = list(subway_data[line].keys())

selected_stations = st.multiselect(
    "비교할 역을 선택하세요.",
    stations,
    default=stations[:2]
)

if selected_stations:
    comparison_data = {}

    for selected_station in selected_stations:
        station_values = subway_data[line][selected_station][day]
        comparison_data[selected_station] = statistics.mean(station_values)

    st.bar_chart(comparison_data)

    best_station = min(
        comparison_data,
        key=comparison_data.get
    )

    st.success(
        f"🏆 평균 혼잡도가 가장 낮은 역은 "
        f"{best_station}입니다! "
        f"(평균 {comparison_data[best_station]:.1f}%)"
    )
else:
    st.warning("비교할 역을 하나 이상 선택해주세요.")

st.divider()

# -----------------------------------
# 혼잡도 안내
# -----------------------------------
st.subheader("📖 혼잡도 기준 안내")

st.write("🟢 0~39% : 여유")
st.write("🟡 40~59% : 보통")
st.write("🟠 60~79% : 혼잡")
st.write("🔴 80~100% : 매우 혼잡")

st.divider()

st.caption(
    "🚇 지하철 혼잡도 분석 프로젝트 | "
    "Python + Streamlit"
)
