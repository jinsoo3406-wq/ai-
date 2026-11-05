
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

# ==================================
# 1. 기본 설정
# ==================================
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("서울시 행정구별 연령대 인구 분석")
st.caption("행정구와 연도를 선택하여 연령대별 인구를 분석합니다.")

# ==================================
# 2. 한글 CSV 인코딩 처리
# ==================================
def load_csv(file):
    encodings = [
        "utf-8-sig",
        "cp949",
        "euc-kr",
        "utf-8"
    ]

    for encoding in encodings:
        try:
            if hasattr(file, "seek"):
                file.seek(0)

            df = pd.read_csv(
                file,
                encoding=encoding
            )
            return df, encoding

        except (UnicodeDecodeError, UnicodeError):
            continue

    raise ValueError("CSV 인코딩을 확인해 주세요.")

# ==================================
# 3. 데이터 불러오기
# ==================================
uploaded_file = st.sidebar.file_uploader(
    "인구 데이터 CSV 업로드",
    type=["csv"]
)

default_file = Path(__file__).parent / "population.csv"

try:
    if uploaded_file is not None:
        df, encoding = load_csv(uploaded_file)

    elif default_file.exists():
        df, encoding = load_csv(
            default_file.open("rb")
        )

    else:
        st.warning("population.csv 파일을 업로드해 주세요.")
        st.stop()

except Exception as e:
    st.error(f"파일 읽기 오류: {e}")
    st.stop()

df.columns = df.columns.astype(str).str.strip()

st.sidebar.success(
    f"한글 인코딩 확인: {encoding}"
)

# ==================================
# 4. 행정구 및 연도 설정
# ==================================
if "행정구역" not in df.columns:
    st.error("'행정구역' 열이 없습니다.")
    st.stop()

df["행정구역표시"] = (
    df["행정구역"]
    .astype(str)
    .str.replace(
        r"\s*\(\d+\)\s*$",
        "",
        regex=True
    )
    .str.strip()
)

years = sorted({
    int(match.group(1))
    for col in df.columns
    if (
        match := re.match(
            r"(\d{4})년_거주자_",
            col
        )
    )
})

districts = sorted(
    df["행정구역표시"].dropna().unique()
)

if not years or not districts:
    st.error("행정구역 또는 연도 데이터를 확인해 주세요.")
    st.stop()

default_district = (
    "서울특별시"
    if "서울특별시" in districts
    else districts[0]
)

# ==================================
# 5. 선택 메뉴
# ==================================
st.sidebar.header("분석 조건")

district = st.sidebar.selectbox(
    "행정구 선택",
    districts,
    index=districts.index(default_district)
)

year = st.sidebar.selectbox(
    "연도 선택",
    years,
    index=len(years) - 1
)

st.sidebar.info(
    "현재 데이터에는 성별 구분이 없어 "
    "행정구와 연도만 선택할 수 있습니다."
)

# ==================================
# 6. 연령대 데이터 추출
# ==================================
age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

selected = df[
    df["행정구역표시"] == district
]

if selected.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

row = selected.iloc[0]

columns = [
    f"{year}년_거주자_{age}"
    for age in age_groups
]

missing = [
    col for col in columns
    if col not in df.columns
]

if missing:
    st.error(f"누락된 열: {missing}")
    st.stop()

values = []

for col in columns:
    value = pd.to_numeric(
        str(row[col]).replace(",", ""),
        errors="coerce"
    )

    values.append(
        0 if pd.isna(value) else int(value)
    )

plot_df = pd.DataFrame({
    "나이": age_groups,
    "인구수": values
})

# ==================================
# 7. 주요 통계
# ==================================
total_col = f"{year}년_거주자_총인구수"

if total_col in df.columns:
    total = pd.to_numeric(
        str(row[total_col]).replace(",", ""),
        errors="coerce"
    )
else:
    total = sum(values)

total = int(total) if pd.notna(total) else sum(values)

peak = plot_df.loc[
    plot_df["인구수"].idxmax()
]

elderly = sum(values[6:])

elderly_ratio = (
    elderly / total * 100
    if total > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "총인구",
    f"{total:,}명"
)

col2.metric(
    "인구 최다 연령대",
    peak["나이"],
    f"{peak['인구수']:,}명"
)

col3.metric(
    "60세 이상 인구 비율",
    f"{elderly_ratio:.1f}%"
)

# ==================================
# 8. 핫핑크 꺾은선 그래프
# ==================================
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=plot_df["나이"],
        y=plot_df["인구수"],
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="#FF1493",
            width=4
        ),
        marker=dict(
            color="#FF1493",
            size=9
        ),
        hovertemplate=(
            "연령대: %{x}<br>"
            "인구수: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)

# 세로축 10만 명 단위
max_value = max(values)
step = 100000

axis_max = max(
    step,
    ((max_value + step - 1) // step) * step
)

fig.update_layout(
    title=f"{district} {year}년 연령대별 인구",
    xaxis_title="나이",
    yaxis_title="인구수(명)",
    template="plotly_white",
    height=600,
    font=dict(
        family="Malgun Gothic, AppleGothic, Noto Sans KR, sans-serif",
        size=13
    ),
    hovermode="x unified"
)

fig.update_xaxes(
    showgrid=True,
    gridcolor="#D3D3D3"
)

fig.update_yaxes(
    tickmode="linear",
    tick0=0,
    dtick=step,
    range=[0, axis_max],
    tickformat=",",
    showgrid=True,
    gridcolor="#D3D3D3"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# 9. 데이터 표
# ==================================
with st.expander("연령대별 인구 데이터 확인"):

    st.dataframe(
        plot_df,
        use_container_width=True
    )

# ==================================
# 10. CSV 다운로드
# ==================================
csv_data = plot_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="분석 데이터 CSV 다운로드",
    data=csv_data,
    file_name=f"{district}_{year}_인구분석.csv",
    mime="text/csv"
)

st.caption(
    "데이터 출처: 업로드한 서울시 인구 CSV"
)
