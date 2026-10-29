import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="MBTI 영화 & 책 추천소 🍿📚", page_icon="🎬")

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
        "title": "🌿 열정적인 중재자 (INFP)",
        "movies": ["월플라워 (The Perks of Being a Wallflower)", "라라랜드 (La La Land)"],
        "books": ["어린 왕자 (앙투안 드 생텍쥐페리)", "호밀밭의 파수꾼 (J.D. 샐린저)", "나의 라임오렌지나무 (J.M. 바스콘셀로스)"]
    },
    "ENFJ": {
        "title": "☀️ 정의로운 사회운동가 (ENFJ)",
        "movies": ["죽은 시인의 사회 (Dead Poets Society)", "위대한 쇼맨"],
        "books": ["아몬드 (손원평)", "자존감 수업 (윤홍균)", "모리와 함께한 화요일 (미치 앨봄)"]
    },
    "ENFP": {
        "title": "🎉 재기발랄한 활동가 (ENFP)",
        "movies": ["월터 M터의 상상은 현실이 된다", "월-E (WALL-E)"],
        "books": ["연금술사 (파울로 코엘료)", "꾸뻬 씨의 행복 여행 (프랑수아 렐로르)", "꽃들에게 희망을 (트리나 포러스)"]
    },
    "ISTJ": {
        "title": "🛡️ 청렴결백한 논리주의자 (ISTJ)",
        "movies": ["쇼생크 탈출 (The Shawshank Redemption)", "설국열차 (Snowpiercer)"],
        "books": ["아주 작은 습관의 힘 (제임스 클리어)", "정의란 무엇인가 (마이클 샌델)", "부자의 행동 패턴 (사이토 히토리)"]
    },
    "ISFJ": {
        "title": "🤝 용감한 수호자 (ISFJ)",
        "movies": ["포레스트 검프 (Forrest Gump)", "리틀 포레스트"],
        "books": ["나미야 잡화점의 기적 (히가시노 게이고)", "불편한 편의점 (김호연)", "당신이 옳다 (정혜신)"]
    },
    "ESTJ": {
        "title": "📊 엄격한 관리자 (ESTJ)",
        "movies": ["파운더 (The Founder)", "인턴 (The Intern)"],
        "books": ["부자 아빠 가난한 아빠 (로버트 기요사키)", "그릿 GRIT (앤절라 더크워스)", "백만장자 시크릿 (하브 에커)"]
    },
    "ESFJ": {
        "title": "💖 사교적인 외교관 (ESFJ)",
        "movies": ["해리 포터와 마법사의 돌", "어바웃 타임 (About Time)"],
        "books": ["할머니가 미안하다고 전해달랬어요 (프레드릭 배크만)", "달러구트 꿈 백화점 (이미예)", "관계의 기술 (존 맥스웰)"]
    },
    "ISTP": {
        "title": "🔧 만능 재주꾼 (ISTP)",
        "movies": ["매드맥스: 분노의 도로", "미션 임파서블: 고스트 프로토콜"],
        "books": ["마션 (앤디 위어)", "이기적 유전자 (리처드 도킨스)", "파이 이야기 (얀 마텔)"]
    },
    "ISFP": {
        "title": "🎨 호기심 많은 예술가 (ISFP)",
        "movies": ["카모메 식당", "소울 (Soul)"],
        "books": ["킨포크 (KINFOLK) 라이프", "지구끝의 온실 (김초엽)", "방구석 미술관 (조원재)"]
    },
    "ESTP": {
        "title": "🔥 모험을 즐기는 사업가 (ESTP)",
        "movies": ["분노의 질주: 더 맥시멈", "탑건: 매버릭"],
        "books": ["역발상 투자의 기술 (켄 피셔)", "아웃라이어 (말콤 글래드웰)", "도둑맞은 집중력 (요한 하리)"]
    },
    "ESFP": {
        "title": "🌟 자유로운 영혼의 연예인 (ESFP)",
        "movies": ["위대한 쇼맨 (The Greatest Showman)", "맘마미아!"],
        "books": ["지금 이 순간을 살아라 (에크하르트 토레)", "지킬 앤 하이드", "행복의 기원 (서은국)"]
    }
}

# 드롭다운으로 MBTI 선택
selected_mbti = st.selectbox("너의 MBTI를 선택해봐! 👇", list(mbti_recommendations.keys()))

# 선택된 MBTI 결과 출력
if selected_mbti:
    info = mbti_recommendations[selected_mbti]
    
    st.markdown(f"## {info['title']}")
    st.write("---")
    
    # 2컬럼 레이아웃으로 영화 / 책 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎬 추천 영화 2편")
        for i, movie in enumerate(info['movies'], 1):
            st.markdown(f"**{i}. {movie}**")
            
    with col2:
        st.subheader("📚 추천 책 3권")
        for i, book in enumerate(info['books'], 1):
            st.markdown(f"**{i}. {book}**")
            
    st.markdown("---")
    st.success("이번 주말엔 이 영화랑 책으로 힐링해 보는 건 어때? 🍿📖")
