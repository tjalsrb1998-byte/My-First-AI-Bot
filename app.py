import streamlit as st
from typing import Dict, List
import json
from pathlib import Path
import re

# -----------------------------
# config.json 저장/불러오기
# -----------------------------
CONFIG_PATH = Path("config.json")


def load_resource_urls() -> Dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("resource_urls", {})
        except Exception:
            return {}
    return {}


def save_resource_urls(resource_urls: Dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"resource_urls": resource_urls}, f, ensure_ascii=False, indent=2)


# -----------------------------
# 유튜브 링크 정규화
# -----------------------------
def normalize_youtube_url(url: str) -> str:
    if not url:
        return ""
    if "youtu.be" in url:
        video_id = url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    if "shorts" in url:
        video_id = url.split("/shorts/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    if "watch?v=" in url:
        video_id = re.search(r"v=([^&]+)", url)
        if video_id:
            return f"https://www.youtube.com/embed/{video_id.group(1)}"
    return url


# -----------------------------
# 발문 카드 데이터
# -----------------------------
def get_default_cards() -> List[Dict]:
    return [
        {
            "id": "obs_sun_appearance",
            "stage": "생각해보기",
            "label": "생각해보기: 계절 변화의 까닭",
            "question": "계절의 변화가 생기는 까닭은 무엇일까요?",
            "resources": [],
        },
        {
            "id": "misconception_distance",
            "stage": "확장",
            "label": "더 생각해보기: 거리 오개념 확인",
            "question": "계절은 지구가 태양에 가까워져서 또는 멀어져서 생긴다고 말해도 될까요?",
            "resources": [],
        },
        {
            "id": "summary_sentence",
            "stage": "정리",
            "label": "정리: 한 문장으로 계절 설명",
            "question": "계절이 생기는 까닭을 한 문장으로 말해 볼까요?",
            "resources": [],
        },
    ]


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "cards" not in st.session_state:
    st.session_state.cards = get_default_cards()

if "resource_urls" not in st.session_state:
    st.session_state.resource_urls = load_resource_urls()

if "selected_card_index" not in st.session_state:
    st.session_state.selected_card_index = 0


def get_resource_url(card_id: str, res_id: str, default_url: str) -> str:
    return st.session_state.resource_urls.get(card_id, {}).get(res_id, default_url)


def set_resource_url(card_id: str, res_id: str, url: str) -> None:
    st.session_state.resource_urls.setdefault(card_id, {})[res_id] = url


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 수업 설정")

    labels = [c["label"] for c in st.session_state.cards]
    selected = st.selectbox(
        "발문 카드 선택",
        range(len(labels)),
        format_func=lambda i: labels[i],
        index=st.session_state.selected_card_index,
    )
    st.session_state.selected_card_index = selected


# -----------------------------
# 메인 레이아웃
# -----------------------------
st.title("🌍 지구, 태양 주위를 떠도는 여정")
st.markdown("---")

card = st.session_state.cards[st.session_state.selected_card_index]

st.markdown(f"### {card['label']}")
st.markdown(f"**{card['question']}**")

answer = st.text_area(
    "",
    key=f"answer_{card['id']}",
    height=100,
    placeholder="예) 여름에는 태양이 더 높이 떠 있어서 햇빛이 강하게 느껴져요.",
)

# -----------------------------
# 버튼 영역
# -----------------------------
col_prev, col_fb, col_res, col_next = st.columns(4)

with col_prev:
    prev_step = st.button("이전 단계로 돌아가기")

with col_fb:
    show_feedback = st.button("피드백 보기")

with col_res:
    show_resources = st.button("추가 자료 보기")

with col_next:
    next_step = st.button("다음 단계로 넘어가기")

# -----------------------------
# 버튼 동작
# -----------------------------
if prev_step:
    st.session_state.selected_card_index = (
        st.session_state.selected_card_index - 1
    ) % len(st.session_state.cards)
    st.rerun()

if next_step:
    st.session_state.selected_card_index = (
        st.session_state.selected_card_index + 1
    ) % len(st.session_state.cards)
    st.rerun()

if show_feedback:
    st.markdown("---")
    st.subheader("💬 교사용 피드백")
    st.write("학생의 생각을 존중하며, 태양의 높이·빛의 각도·자전축 기울기로 사고를 확장해 주세요.")

if show_resources:
    st.markdown("---")
    st.subheader("📚 추가 자료")
    st.info("사이드바에서 자료 URL을 설정할 수 있습니다.")
