const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// 환경 변수 로드
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Google Gemini API 초기화
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

// 챗봇 API 엔드포인트
app.post('/api/chat', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    if (!process.env.GOOGLE_API_KEY || process.env.GOOGLE_API_KEY === 'your_google_api_key_here') {
      return res.status(500).json({ 
        error: 'Google API key is not configured. Please set GOOGLE_API_KEY in .env file.' 
      });
    }

    // Gemini 모델 가져오기
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    // 대화 히스토리 구성
    const chatHistory = history.map(msg => ({
      role: msg.role === 'user' ? 'user' : 'model',
      parts: [{ text: msg.content }]
    }));

    // 현재 메시지 추가
    const currentMessage = { role: 'user', parts: [{ text: message }] };

    // 채팅 시작
    const chat = model.startChat({
      history: chatHistory,
    });

    // 메시지 전송 및 응답 받기
    const result = await chat.sendMessage(message);
    const response = await result.response;
    const text = response.text();

    res.json({
      response: text,
      success: true
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ 
      error: 'Failed to get response from Gemini API',
      details: error.message 
    });
  }
});

// 헬스 체크 엔드포인트
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok',
    apiKeyConfigured: !!process.env.GOOGLE_API_KEY && process.env.GOOGLE_API_KEY !== 'your_google_api_key_here'
  });
});

// 루트 경로 - index.html 제공
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/chatbot.html');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Make sure to set GOOGLE_API_KEY in .env file`);
});

