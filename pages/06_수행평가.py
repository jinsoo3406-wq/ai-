
import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 탐험 🌈",
    page_icon="🔮",
    layout="centered"
)

# CSS 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff0f6, #e8f4ff);
}
.main-title {
    text-align: center;
    color: #7357c8;
    font-size: 38px;
    font-weight: bold;
}
.sub-title {
    text-align: center;
    color: #777;
    font-size: 17px;
}
.result-box {
    background-color: white;
    padding: 22px;
    border-radius: 18px;
    border: 2px solid #eadcff;
    margin: 10px 0;
}
.emoji {
    font-size: 65px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# MBTI별 정보
mbti_data = {
    "ISTJ": {
        "emoji": "📋",
        "nickname": "꼼꼼한 현실주의자",
        "personality": "책임감이 강하고 계획적으로 행동해요. 맡은 일은 끝까지 해내는 믿음직한 스타일!",
        "majors": ["경영학과", "회계학과", "행정학과", "법학과"],
        "careers": [
            ("회계사 💰", "숫자를 정확하게 분석하고 꼼꼼하게 일하는 사람"),
            ("공무원 🏛️", "책임감이 강하고 규칙과 원칙을 잘 지키는 사람"),
            ("데이터 분석가 📊", "논리적으로 자료를 분석하고 문제를 해결하는 사람")
        ]
    },
    "ISFJ": {
        "emoji": "🧸",
        "nickname": "따뜻한 수호자",
        "personality": "배려심이 많고 다른 사람을 잘 챙겨요. 조용하지만 따뜻한 마음을 가진 스타일!",
        "majors": ["간호학과", "사회복지학과", "교육학과", "유아교육과"],
        "careers": [
            ("간호사 🏥", "세심하고 책임감 있으며 다른 사람을 돌보는 것을 좋아하는 사람"),
            ("교사 🍎", "학생을 배려하고 차근차근 설명하는 것을 좋아하는 사람"),
            ("사회복지사 💗", "도움이 필요한 사람에게 관심을 가지고 공감하는 사람")
        ]
    },
    "INFJ": {
        "emoji": "🦋",
        "nickname": "통찰력 있는 조언자",
        "personality": "상상력이 풍부하고 다른 사람의 마음을 잘 이해해요. 자신만의 가치관이 뚜렷한 스타일!",
        "majors": ["심리학과", "상담학과", "사회학과", "교육학과"],
        "careers": [
            ("심리상담사 🧠", "다른 사람의 감정을 이해하고 진심으로 공감하는 사람"),
            ("작가 ✍️", "생각이 깊고 자신의 생각을 글로 표현하는 사람"),
            ("사회문제 연구원 🌍", "세상을 더 좋은 방향으로 바꾸고 싶어 하는 사람")
        ]
    },
    "INTJ": {
        "emoji": "♟️",
        "nickname": "전략적인 설계자",
        "personality": "분석적이고 독립적인 성향이에요. 목표를 세우고 효율적인 방법을 찾는 것을 좋아해요!",
        "majors": ["컴퓨터공학과", "수학과", "경제학과", "건축학과"],
        "careers": [
            ("소프트웨어 개발자 💻", "논리적으로 생각하고 복잡한 문제를 해결하는 사람"),
            ("연구원 🔬", "깊이 탐구하고 새로운 지식을 발견하는 것을 좋아하는 사람"),
            ("전략기획자 🎯", "미래를 예측하고 체계적으로 계획하는 사람")
        ]
    },
    "ISTP": {
        "emoji": "🛠️",
        "nickname": "만능 재주꾼",
        "personality": "호기심이 많고 직접 경험하며 배우는 것을 좋아해요. 위기 상황에서도 침착한 스타일!",
        "majors": ["기계공학과", "자동차공학과", "컴퓨터공학과", "항공우주공학과"],
        "careers": [
            ("기계공학자 ⚙️", "기계의 원리를 이해하고 직접 설계하는 것을 좋아하는 사람"),
            ("정비사 🔧", "기계를 다루고 고장 난 부분을 해결하는 것을 좋아하는 사람"),
            ("개발자 💻", "실용적인 기술을 활용해 문제를 해결하는 사람")
        ]
    },
    "ISFP": {
        "emoji": "🎨",
        "nickname": "자유로운 예술가",
        "personality": "감성이 풍부하고 자신만의 개성을 중요하게 생각해요. 아름다운 것을 발견하는 감각이 뛰어나요!",
        "majors": ["디자인학과", "미술학과", "패션디자인학과", "음악학과"],
        "careers": [
            ("디자이너 🎨", "창의적이고 색감과 형태에 대한 감각이 좋은 사람"),
            ("사진작가 📸", "순간의 아름다움을 발견하고 표현하는 사람"),
            ("패션디자이너 👗", "자신만의 스타일과 감각을 표현하는 사람")
        ]
    },
    "INFP": {
        "emoji": "🌷",
        "nickname": "열정적인 중재자",
        "personality": "감수성이 풍부하고 상상력이 뛰어나요. 자신만의 신념과 꿈을 소중하게 생각하는 스타일!",
        "majors": ["문예창작학과", "심리학과", "국어국문학과", "영상학과"],
        "careers": [
            ("작가 📖", "상상력이 풍부하고 감정을 글로 표현하는 사람"),
            ("콘텐츠 기획자 🎬", "새로운 아이디어를 생각하고 이야기를 만드는 사람"),
            ("상담 전문가 💕", "다른 사람의 고민을 들어주고 공감하는 사람")
        ]
    },
    "INTP": {
        "emoji": "🧪",
        "nickname": "논리적인 사색가",
        "personality": "지적 호기심이 많고 새로운 원리를 탐구하는 것을 좋아해요. 독창적인 아이디어가 많은 스타일!",
        "majors": ["물리학과", "컴퓨터공학과", "철학과", "수학과"],
        "careers": [
            ("과학자 🔬", "호기심을 가지고 새로운 원리를 탐구하는 사람"),
            ("프로그래머 💻", "논리적인 사고로 복잡한 문제를 해결하는 사람"),
            ("데이터 과학자 📈", "정보를 분석하고 새로운 규칙을 발견하는 사람")
        ]
    },
    "ESTP": {
        "emoji": "🔥",
        "nickname": "에너지 넘치는 모험가",
        "personality": "활동적이고 도전을 즐겨요. 새로운 상황에 빠르게 적응하고 행동력이 뛰어난 스타일!",
        "majors": ["체육학과", "경영학과", "스포츠과학과", "경찰행정학과"],
        "careers": [
            ("스포츠 지도자 ⚽", "활동적이고 사람들과 함께 움직이는 것을 좋아하는 사람"),
            ("사업가 🚀", "도전을 두려워하지 않고 실행력이 뛰어난 사람"),
            ("경찰관 👮", "순발력이 좋고 현장에서 빠르게 판단하는 사람")
        ]
    },
    "ESFP": {
        "emoji": "🎉",
        "nickname": "자유로운 연예인",
        "personality": "밝고 사교적이며 사람들과 어울리는 것을 좋아해요. 주변을 즐겁게 만드는 분위기 메이커!",
        "majors": ["방송연예과", "공연예술학과", "광고홍보학과", "관광학과"],
        "careers": [
            ("방송인 🎤", "표현력이 좋고 사람들 앞에 서는 것을 즐기는 사람"),
            ("이벤트 기획자 🎊", "사람들에게 즐거운 경험을 만들어 주는 사람"),
            ("호텔리어 🏨", "친절하고 다양한 사람들과 소통하는 것을 좋아하는 사람")
        ]
    },
    "ENFP": {
        "emoji": "🌈",
        "nickname": "재기발랄한 활동가",
        "personality": "호기심이 많고 새로운 도전을 좋아해요. 아이디어가 넘치고 사람들과 소통하는 것을 즐겨요!",
        "majors": ["광고홍보학과", "미디어학과", "심리학과", "문화콘텐츠학과"],
        "careers": [
            ("광고기획자 💡", "창의적인 아이디어와 소통 능력을 가진 사람"),
            ("유튜버 📹", "자신만의 콘텐츠를 만들고 사람들과 소통하는 사람"),
            ("마케터 📱", "트렌드에 민감하고 새로운 아이디어를 실현하는 사람")
        ]
    },
    "ENTP": {
        "emoji": "⚡",
        "nickname": "뜨거운 논쟁을 즐기는 변론가",
        "personality": "재치 있고 창의적이에요. 기존의 방식에 질문을 던지고 새로운 가능성을 찾는 스타일!",
        "majors": ["창업학과", "경영학과", "법학과", "광고홍보학과"],
        "careers": [
            ("창업가 🚀", "새로운 아이디어를 실현하고 도전하는 사람"),
            ("변호사 ⚖️", "논리적으로 주장하고 토론하는 것을 좋아하는 사람"),
            ("기획자 💡", "다양한 아이디어를 연결하고 새로운 전략을 만드는 사람")
        ]
    },
    "ESTJ": {
        "emoji": "👑",
        "nickname": "엄격한 관리자",
        "personality": "체계적이고 리더십이 있어요. 목표를 정하고 사람들과 함께 결과를 만들어 가는 스타일!",
        "majors": ["경영학과", "행정학과", "경찰행정학과", "경제학과"],
        "careers": [
            ("경영 관리자 📊", "조직을 체계적으로 운영하고 책임감이 강한 사람"),
            ("군인 🎖️", "규칙을 잘 지키고 조직생활에 책임감을 가진 사람"),
            ("프로젝트 관리자 📅", "계획을 세우고 팀원들과 목표를 달성하는 사람")
        ]
    },
    "ESFJ": {
        "emoji": "💖",
        "nickname": "사교적인 외교관",
        "personality": "친절하고 사교적이에요. 주변 사람들을 잘 챙기며 협력하는 것을 좋아하는 스타일!",
        "majors": ["교육학과", "간호학과", "호텔경영학과", "사회복지학과"],
        "careers": [
            ("교사 🍎", "다른 사람을 돕고 함께 성장하는 것을 좋아하는 사람"),
            ("인사 담당자 🤝", "사람들과 소통하고 협력하는 것을 좋아하는 사람"),
            ("간호사 🩺", "배려심이 많고 세심하게 사람을 돌보는 사람")
        ]
    },
    "ENFJ": {
        "emoji": "🌟",
        "nickname": "정의로운 사회운동가",
        "personality": "공감 능력이 뛰어나고 사람들에게 긍정적인 영향을 주고 싶어 해요. 리더십과 소통 능력이 좋은 스타일!",
        "majors": ["교육학과", "심리학과", "사회복지학과", "정치외교학과"],
        "careers": [
            ("교육 전문가 🎓", "다른 사람의 성장을 돕고 이끄는 것을 좋아하는 사람"),
            ("상담사 💗", "공감 능력이 뛰어나고 다른 사람의 이야기를 잘 듣는 사람"),
            ("외교관 🌏", "소통 능력이 뛰어나고 다양한 문화를 이해하는 사람")
        ]
    },
    "ENTJ": {
        "emoji": "🚀",
        "nickname": "대담한 통솔자",
        "personality": "목표 지향적이고 추진력이 강해요. 큰 그림을 보고 사람들을 이끄는 것을 좋아하는 스타일!",
        "majors": ["경영학과", "경제학과", "정치외교학과", "산업공학과"],
        "careers": [
            ("CEO 🏢", "리더십과 결단력이 있고 목표를 향해 도전하는 사람"),
            ("기업 컨설턴트 📈", "문제를 분석하고 효과적인 해결책을 제시하는 사람"),
            ("변호사 ⚖️", "논리적이고 자신감 있게 의견을 전달하는 사람")
        ]
    }
}


# 화면 제목
st.markdown(
    '<div class="main-title">🔮 MBTI 진로 탐험 🌈</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">나에게 어울리는 직업과 학과는 무엇일까? 💖</div>',
    unsafe_allow_html=True
)

st.write("")
st.info("✨ 나의 MBTI를 선택하고 미래의 진로를 탐험해 보자!")

# MBTI 선택
mbti = st.selectbox(
    "🧩 나의 MBTI를 선택해 줘!",
    list(mbti_data.keys()),
    index=None,
    placeholder="MBTI 유형을 선택해 주세요."
)

# 결과 출력
if mbti:

    data = mbti_data[mbti]

    st.divider()

    st.markdown(
        f'<div class="emoji">{data["emoji"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h2 style='text-align:center; color:#7357c8;'>"
        f"{mbti} - {data['nickname']}</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-box">'
        f'<h3>💖 나의 성격은?</h3>'
        f'<p>{data["personality"]}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    # 학과 추천
    st.subheader("📚 나에게 어울리는 대학교 학과")

    for major in data["majors"]:
        st.markdown(f"- 🎓 **{major}**")

    # 진로 추천
    st.subheader("🚀 나에게 어울리는 직업 TOP 3")

    for i, (career, description) in enumerate(data["careers"], 1):
        with st.expander(f"{i}위. {career}"):
            st.write(f"💡 **이런 사람이 잘 어울려요!**")
            st.write(description)

    st.divider()

    st.success(
        f"🎉 {mbti} 유형의 진로 탐험 완료! "
        "나만의 멋진 미래를 만들어 보자!"
    )

    st.caption(
        "※ MBTI는 자기 이해를 위한 참고 자료예요. "
        "실제 적성과 진로는 개인의 관심사, 능력, 경험에 따라 달라질 수 있어요."
    )

else:
    st.markdown("""
    <div class="result-box" style="text-align:center;">
        <h2>🌷 아직 MBTI를 선택하지 않았어요!</h2>
        <p>위에서 나의 MBTI를 선택하면</p>
        <p>나에게 어울리는 이모지와 진로를 알려줄게요! 💕</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center;'>"
        "🌈 💖 🎨 🚀 🌻</h1>",
        unsafe_allow_html=True
    )
