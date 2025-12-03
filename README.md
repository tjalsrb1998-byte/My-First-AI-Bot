# Google Gemini AI Chatbot

Google Gemini API를 사용하는 Streamlit 기반 웹 챗봇 애플리케이션입니다.

## 기능

- 🤖 Google Gemini 2.5 Flash 모델을 사용한 AI 챗봇
- 💬 실시간 대화 인터페이스
- 🎨 Streamlit의 모던한 UI
- 🔒 안전한 API 키 관리 (.env 파일 또는 사이드바 입력)
- 📱 반응형 디자인

## 시작하기

### 1. Python 가상환경 생성 (선택사항)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 열고 Google API 키를 입력하세요:

```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

Google API 키는 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받을 수 있습니다.

**또는** Streamlit 앱 실행 후 사이드바에서 직접 입력할 수도 있습니다.

### 4. Streamlit 앱 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리고 `http://localhost:8501`에서 앱이 실행됩니다.

## 프로젝트 구조

```
My-First-AI-Bot/
├── app.py              # Streamlit 메인 앱
├── requirements.txt    # Python 의존성
├── .env               # 환경 변수 (API 키)
├── .gitignore         # Git 제외 파일 목록
├── index.html         # 단일 HTML 파일 버전 (선택사항)
└── README.md          # 프로젝트 문서
```

## 사용 방법

1. Streamlit 앱을 실행합니다
2. 사이드바에서 Google API 키를 입력합니다 (또는 .env 파일에 설정)
3. 메시지를 입력하고 전송합니다
4. Gemini AI가 응답합니다
5. 대화 기록은 세션 동안 유지됩니다

## 기술 스택

- **프레임워크**: Streamlit
- **AI**: Google Gemini 2.5 Flash API
- **언어**: Python 3.7+
- **환경 변수 관리**: python-dotenv
- **HTTP 요청**: requests

## 주요 라이브러리

- `streamlit`: 웹 앱 프레임워크
- `requests`: HTTP 요청
- `python-dotenv`: 환경 변수 관리

## 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요. 이미 `.gitignore`에 포함되어 있습니다.
- API 키를 안전하게 관리하세요.
- Streamlit은 개발용으로 설계되었습니다. 프로덕션 환경에서는 추가적인 보안 조치를 고려하세요.

## 라이선스

MIT
