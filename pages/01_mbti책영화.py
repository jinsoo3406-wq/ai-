import streamlit as st

# 페이지 기본 설정
st.set_page_title("MBTI 영화 & 책 추천소 🍿📚", page_icon="🎬")

# 상단 타이틀 영역
st.title("🎬 MBTI 맞춤 영화 & 책 방구석 추천소 📚")
st.markdown("너의 MBTI를 고르면 취향저격 **영화 2편**과 **책 3권**을 싹 다 정리해서 알려줄게! ✨")
st.markdown("---")

# MBTI별 영화(2개) & 책(3권) 추천 데이터베이스
mbti_recommendations = {
    "INTJ": {
        "title": "🧠 용의주도한 전략가 (INTJ)",
        "movies": ["인셉션 (Inception)", "마션 (The Martian)"],
        "books": ["사피엔스 (유발 하라리)", "1984 (조지 오웰)", "코스모스 (칼 세이건)"]
    },
    "INTP": {
        "title": "🔬 논리적인 사색가 (INTP)",
        "movies": ["인터스텔라 (Interstellar)", "매트릭스 (The Matrix)"],
        "books": ["이기적 유전자 (리처드 도킨스)", "평행우주 (미치오 카쿠)", "물고기는 존재하지 않는다 (룰루 밀러)"]
    },
    "ENTJ": {
        "title": "👑 대담한 통솔자 (ENTJ)",
        "movies": ["소셜 네트워크 (The Social Network)", "머니볼 (Moneyball)"],
        "books": ["군주론 (니콜로 마키아벨리)", "원씽 (게리 켈러)", "원칙 (레이 달리오)"]
    },
    "ENTP": {
        "title": "💡 뜨거운 논쟁을 즐기는 변론가 (ENTP)",
        "movies": ["캐치 미 이프 유 캔 (Catch Me If You Can)", "빅쇼트 (The Big Short)"],
        "books": ["총 균 쇠 (재레드 다이아몬드)", "생각에 관한 생각 (대니얼 카너먼)", "설득의 심리학 (로버트 치알디니)"]
    },
    "INFJ": {
        "title": "✨ 선의의 옹호자 (INFJ)",
        "movies": ["트루먼 쇼 (The Truman Show)", "센과 치히로의 행방불명"],
        "books": ["데미안 (헤르만 헤세)", "미움받을 용기 (기시미 이치로)", "참을 수 없는 존재의 가벼움 (밀란 쿤데라)"]
    },
    "INFP": {
        "
