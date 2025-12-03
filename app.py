import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Gemini API 설정
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# System Instruction - 친절한 5년 차 초등학교 선생님
SYSTEM_INSTRUCTION = """당신은 친절하고 경험이 풍부한 5년 차 초등학교 선생님입니다. 
다음과 같은 특징을 가지고 있습니다:

1. 항상 따뜻하고 친절한 말투를 사용합니다
2. 아이들의 눈높이에 맞춰 쉽고 이해하기 쉽게 설명합니다
3. 격려와 칭찬을 아끼지 않습니다
4. 어려운 내용도 쉽게 풀어서 설명할 수 있습니다
5. 학생들의 질문에 인내심을 가지고 답변합니다
6. 때로는 유머를 섞어서 재미있게 설명합니다
7. 배움에 대한 열정과 긍정적인 에너지를 전달합니다

항상 "선생님"이라는 정체성을 유지하며, 학생들을 가르치고 도와주는 마음으로 대화하세요."""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GOOGLE_API_KEY", "")

# 사이드바 - API 키 설정
with st.sidebar:
    st.header("⚙️ 설정")
    st.markdown("---")
    
    # API 키 입력
    api_key_input = st.text_input(
        "Google API 키",
        value=st.session_state.api_key if st.session_state.api_key else "",
        type="password",
        help="Google AI Studio에서 발급받은 API 키를 입력하세요"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✓ API 키가 설정되었습니다")
    
    if st.button("🗑️ 대화 기록 지우기"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📖 사용 방법")
    st.markdown("""
    1. Google API 키를 입력하세요
    2. 메시지를 입력하고 전송하세요
    3. Gemini AI가 응답합니다
    """)
    
    st.markdown("---")
    st.markdown("**API 키 발급:**")
    st.markdown("[Google AI Studio](https://makersuite.google.com/app/apikey)")

# 메인 타이틀
st.title("👩‍🏫 친절한 선생님 챗봇")
st.markdown("Google Gemini 2.5 Flash를 사용한 AI 챗봇 - 친절한 5년 차 초등학교 선생님")

# API 키 확인
if not st.session_state.api_key:
    st.warning("⚠️ 사이드바에서 Google API 키를 입력해주세요.")
    st.stop()

# Gemini API 호출 함수
def call_gemini_api(message, api_key):
    """Gemini API를 호출하여 응답을 받아옵니다."""
    url = f"{GEMINI_API_URL}?key={api_key}"
    
    # 대화 히스토리 구성
    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    
    # 현재 메시지 추가
    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })
    
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        }
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("candidates") and len(data["candidates"]) > 0:
            if data["candidates"][0].get("content"):
                return data["candidates"][0]["content"]["parts"][0]["text"]
        
        raise Exception("Invalid response from API")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API 호출 오류: {str(e)}")

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            try:
                response = call_gemini_api(prompt, st.session_state.api_key)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

