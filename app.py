import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="지구, 태양 주위를 떠도는 여정!",
    page_icon="🌍",
    layout="wide"
)

# 메인 타이틀
st.title("🌍 지구, 태양 주위를 떠도는 여정!")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    st.markdown("여기에 설정 옵션을 추가하세요")

# 메인 컨텐츠 영역
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 기능 1")
    st.write("여기에 첫 번째 기능을 구현하세요")
    
    # 예시: 텍스트 입력
    user_input = st.text_input("입력해주세요", placeholder="텍스트를 입력하세요")
    if user_input:
        st.success(f"입력하신 내용: {user_input}")

with col2:
    st.subheader("📈 기능 2")
    st.write("여기에 두 번째 기능을 구현하세요")
    
    # 예시: 버튼
    if st.button("클릭하세요"):
        st.balloons()
        st.info("버튼이 클릭되었습니다!")

# 하단 영역
st.markdown("---")
st.markdown("### 추가 기능")
st.write("여기에 더 많은 기능을 추가할 수 있습니다")

# 파일이 변경되었습니다 - Streamlit이 자동으로 리로드합니다

