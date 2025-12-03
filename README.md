# Google Gemini AI Chatbot

Google Gemini API를 사용하는 모던한 웹 챗봇 애플리케이션입니다.

## 기능

- 🤖 Google Gemini Pro 모델을 사용한 AI 챗봇
- 💬 실시간 대화 인터페이스
- 🎨 모던하고 반응형 디자인
- 🔒 안전한 API 키 관리 (서버 사이드)

## 시작하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env` 파일을 열고 Google API 키를 입력하세요:

```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

Google API 키는 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받을 수 있습니다.

### 3. 서버 실행

```bash
npm start
```

서버가 `http://localhost:3000`에서 실행됩니다.

### 4. 브라우저에서 접속

브라우저에서 `http://localhost:3000`을 열어 챗봇을 사용하세요.

## 프로젝트 구조

```
My-First-AI-Bot/
├── server.js          # Express 서버 및 API 엔드포인트
├── package.json       # 프로젝트 의존성
├── .env              # 환경 변수 (API 키)
├── .gitignore        # Git 제외 파일 목록
├── public/
│   └── chatbot.html  # 챗봇 프론트엔드 UI
└── README.md         # 프로젝트 문서
```

## API 엔드포인트

### POST /api/chat

챗봇과 대화하기

**요청 본문:**
```json
{
  "message": "안녕하세요!",
  "history": [
    {
      "role": "user",
      "content": "이전 메시지"
    },
    {
      "role": "assistant",
      "content": "이전 응답"
    }
  ]
}
```

**응답:**
```json
{
  "response": "안녕하세요! 무엇을 도와드릴까요?",
  "success": true
}
```

### GET /api/health

서버 상태 확인

**응답:**
```json
{
  "status": "ok",
  "apiKeyConfigured": true
}
```

## 기술 스택

- **백엔드**: Node.js, Express
- **AI**: Google Gemini API (@google/generative-ai)
- **프론트엔드**: HTML5, CSS3, JavaScript (Vanilla)
- **환경 변수 관리**: dotenv

## 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요. 이미 `.gitignore`에 포함되어 있습니다.
- API 키를 안전하게 관리하세요.
- 프로덕션 환경에서는 추가적인 보안 조치를 고려하세요.

## 라이선스

MIT

