
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# =====================================
# 1. 페이지 설정
# =====================================
st.set_page_config(
    page_title="서울 월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 월별 기온분석")
st.write("서울의 월별 및 연도별 기온을 분석하고 두 연도를 비교합니다.")

# =====================================
# 2. CSV 파일 불러오기
# =====================================
@st.cache_data
def load_data(file_path):

    encodings = ["cp949", "euc-kr", "utf-8-sig", "utf-8"]

    for encoding in encodings:
        try:
            return pd.read_csv(
                file_path,
                encoding=encoding,
                header=None
            )
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 인코딩을 확인해주세요.")


uploaded_file = st.sidebar.file_uploader(
    "기온 데이터 CSV 업로드",
    type=["csv"]
)

if uploaded_file is not None:
    raw = None

    for encoding in ["cp949", "euc-kr", "utf-8-sig", "utf-8"]:
        try:
            uploaded_file.seek(0)
            raw = pd.read_csv(
                uploaded_file,
                encoding=encoding,
                header=None
            )
            break
        except UnicodeDecodeError:
            continue

    if raw is None:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.stop()

else:
    file_path = Path(__file__).parent / "trmperature.csv"

    if not file_path.exists():
        st.warning("trmperature.csv 파일을 업로드해주세요.")
        st.stop()

    raw = load_data(str(file_path))


# =====================================
# 3. 데이터 전처리
# =====================================
if raw.shape[1] < 10:
    st.error("CSV 파일의 열 개수가 올바르지 않습니다.")
    st.stop()

df = raw.iloc[:, :10].copy()

df.columns = [
    "지점번호",
    "지역",
    "연월",
    "평균기온",
    "평균최고기온",
    "최고기온",
    "최고기온일자",
    "평균최저기온",
    "최저기온",
    "최저기온일자"
]

# 숫자형 변환
temperature_columns = [
    "평균기온",
    "평균최고기온",
    "최고기온",
    "평균최저기온",
    "최저기온"
]

for col in temperature_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# 날짜 변환
df["최고기온일자"] = pd.to_datetime(
    df["최고기온일자"],
    errors="coerce"
)

df["최저기온일자"] = pd.to_datetime(
    df["최저기온일자"],
    errors="coerce"
)

# 결측치 제거
df = df.dropna(
    subset=["최고기온일자"]
).copy()

# 연도와 월 추출
df["연도"] = df["최고기온일자"].dt.year
df["월"] = df["최고기온일자"].dt.month

# 서울 데이터만 추출
df["지역"] = df["지역"].astype(str).str.strip()

df = df[df["지역"] == "서울"].copy()

if df.empty:
    st.error("서울 데이터가 없습니다.")
    st.stop()

# =====================================
# 4. 월 이름 설정
# =====================================
month_names = {
    1: "1월",
    2: "2월",
    3: "3월",
    4: "4월",
    5: "5월",
    6: "6월",
    7: "7월",
    8: "8월",
    9: "9월",
    10: "10월",
    11: "11월",
    12: "12월"
}

months = list(range(1, 13))

# =====================================
# 5. 서울 월별 기온 그래프
# =====================================
st.header("① 서울 월별 기온 그래프")

st.write(
    "서울의 1월부터 12월까지 월별 평균기온을 분석합니다."
)

monthly = (
    df.groupby("월")
    .agg(
        평균기온=("평균기온", "mean"),
        평균최고기온=("평균최고기온", "mean"),
        평균최저기온=("평균최저기온", "mean")
    )
    .reindex(months)
    .reset_index()
)

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=monthly["월"],
        y=monthly["평균기온"],
        mode="lines+markers",
        name="평균기온",
        line=dict(color="royalblue", width=3)
    )
)

fig1.add_trace(
    go.Scatter(
        x=monthly["월"],
        y=monthly["평균최고기온"],
        mode="lines+markers",
        name="평균최고기온",
        line=dict(color="hotpink", width=3)
    )
)

fig1.add_trace(
    go.Scatter(
        x=monthly["월"],
        y=monthly["평균최저기온"],
        mode="lines+markers",
        name="평균최저기온",
        line=dict(color="skyblue", width=3)
    )
)

fig1.update_layout(
    title="서울 월별 기온 그래프",
    xaxis_title="월",
    yaxis_title="온도 (℃)",
    xaxis=dict(
        tickmode="array",
        tickvals=months,
        ticktext=[month_names[m] for m in months]
    ),
    legend_title="범례",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================
# 6. 연도별 최고기온과 최저기온
# =====================================
st.header("② 연도별 최고기온과 최저기온")

st.write(
    "각 연도에 기록된 가장 높은 기온과 가장 낮은 기온을 비교합니다."
)

yearly = (
    df.groupby("연도")
    .agg(
        최고기온=("최고기온", "max"),
        최저기온=("최저기온", "min")
    )
    .reset_index()
    .sort_values("연도")
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=yearly["연도"],
        y=yearly["최고기온"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="hotpink", width=3),
        marker=dict(size=8)
    )
)

fig2.add_trace(
    go.Scatter(
        x=yearly["연도"],
        y=yearly["최저기온"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="skyblue", width=3),
        marker=dict(size=8)
    )
)

fig2.update_layout(
    title="연도별 최고·최저기온 그래프",
    xaxis_title="연도",
    yaxis_title="온도 (℃)",
    legend_title="범례",
    hovermode="x unified",
    template="plotly_white"
)

fig2.update_xaxes(dtick=1)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.dataframe(
    yearly,
    use_container_width=True,
    hide_index=True
)

# =====================================
# 7. 두 연도 선택 및 비교
# =====================================
st.header("③ 두 연도 기온 비교")

years = sorted(
    df["연도"].dropna().astype(int).unique().tolist()
)

if len(years) < 2:

    st.warning("비교할 수 있는 연도가 2개 이상 필요합니다.")

else:

    default_years = years[-2:]

    selected_years = st.multiselect(
        "비교할 연도 2개를 선택하세요.",
        options=years,
        default=default_years,
        max_selections=2
    )

    if len(selected_years) == 2:

        compare_df = df[
            df["연도"].isin(selected_years)
        ]

        compare = (
            compare_df.groupby(["연도", "월"])
            .agg(
                최고기온=("최고기온", "max"),
                최저기온=("최저기온", "min")
            )
            .reset_index()
        )

        fig3 = go.Figure()

        colors = ["hotpink", "skyblue"]

        for i, year in enumerate(sorted(selected_years)):

            year_data = compare[
                compare["연도"] == year
            ].sort_values("월")

            fig3.add_trace(
                go.Scatter(
                    x=year_data["월"],
                    y=year_data["최고기온"],
                    mode="lines+markers",
                    name=f"{year}년 최고기온",
                    line=dict(
                        color=colors[i],
                        width=3
                    )
                )
            )

            fig3.add_trace(
                go.Scatter(
                    x=year_data["월"],
                    y=year_data["최저기온"],
                    mode="lines+markers",
                    name=f"{year}년 최저기온",
                    line=dict(
                        color=colors[i],
                        width=3,
                        dash="dash"
                    )
                )
            )

        fig3.update_layout(
            title=(
                f"{selected_years[0]}년과 "
                f"{selected_years[1]}년 월별 기온 비교"
            ),
            xaxis_title="월",
            yaxis_title="온도 (℃)",
            xaxis=dict(
                tickmode="array",
                tickvals=months,
                ticktext=[
                    month_names[m] for m in months
                ]
            ),
            legend_title="범례",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    else:

        st.info("비교할 연도를 정확히 2개 선택해주세요.")

# =====================================
# 8. 데이터 정보
# =====================================
st.divider()

st.subheader("데이터 정보")

col1, col2, col3 = st.columns(3)

col1.metric(
    "데이터 개수",
    f"{len(df)}개"
)

col2.metric(
    "분석 연도 수",
    f"{df['연도'].nunique()}년"
)

col3.metric(
    "분석 지역",
    "서울"
)

st.caption(
    "자료: 서울 기온 CSV 데이터"
)
