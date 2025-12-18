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
    payload = {"resource_urls": resource_urls}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# -----------------------------
# 유튜브 URL 정규화
# -----------------------------
def normalize_youtube_url(url: str) -> str:
    if not url:
        return url

    if "youtube.com/watch" in url:
        video_id = re.search(r"v=([^&]+)", url)
        if video_id:
            return f"https://www.youtube.com/embed/{video_id.group(1)}"

    if "youtube.com/shorts" in url:
        video_id = url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"

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
            "expected_answers": [],
            "feedback_rules": {},
            "resources": [],
            "teacher_notes": {},
        },
        {
            "id": "misconception_distance",
            "stage": "확장",
            "label": "더 생각해보기: 거리 오개념 확인",
            "question": "계절은 지구가 태양에 가까워져서 또는 멀어져서 생긴다고 말해도 될까요?",
            "expected_answers": [],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "summary_video",
                    "title": "계절 개념 요약 영상",
                    "type": "video",
                    "default_url": "https://www.youtube.com/shorts/WOEU2LEl5ug",
                }
            ],
            "teacher_notes": {},
        },
        {
            "id": "summary_sentence",
            "stage": "정리",
            "label": "정리: 한 문장으로 계절 설명",
            "question": "계절이 생기는 까닭을 한 문장으로 말해 볼까요?",
            "expected_answers": [],
            "feedback_rules": {},
            "resources": [],
            "teacher_notes": {},
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


def get_resource_url(card_id: str, res: Dict) -> str:
    card_urls = st.session_state.resource_urls.setdefault(card_id, {})
    return card_urls.get(res["id"], res.get("default_url", ""))


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 수업 설정")

    labels = [c["label"] for c in st.session_state.cards]
    selected_index = st.selectbox(
        "발문 카드 선택",
        range(len(labels)),
        format_func=lambda i: labels[i],
        index=st.session_state.selected_card_index,
    )
    st.session_state.selected_card_index = selected_index
    current_card = st.session_state.cards[selected_index]

    st.markdown("---")
    st.subheader("📎 자료 링크 설정")

    for res in current_card.get("resources", []):
        current_url = get_resource_url(current_card["id"], res)
        new_url = st.text_input(
            f"{res['title']} URL",
            value=current_url,
            key=f"url_{current_card['id']}_{res['id']}",
        )
        st.session_state.resource_urls.setdefault(current_card["id"], {})[res["id"]] = new_url

    if st.button("💾 저장"):
        save_resource_urls(st.session_state.resource_urls)
        st.success("저장되었습니다.")


# -----------------------------
# 메인 화면
# -----------------------------
st.title("🌍 지구, 태양 주위를 떠도는 여정")
st.markdown("---")

card = st.session_state.cards[st.session_state.selected_card_index]

st.markdown(f"### {card['label']}")
st.markdown(f"**{card['question']}**")

answer = st.text_area(
    "학생이 실제로 말한 내용을 그대로 적어 주세요.",
    height=100,
)

# 버튼 영역 (순서 + 간격 동일)
col_prev, col_fb, col_res, col_next = st.columns(4)

with col_prev:
    if st.button("이전 단계로 돌아가기"):
        if st.session_state.selected_card_index > 0:
            st.session_state.selected_card_index -= 1
            st.rerun()

with col_fb:
    show_feedback = st.button("피드백 보기")

with col_res:
    show_resources = st.button("추가 자료 보기")

with col_next:
    if st.button("다음 단계로 넘어가기"):
        st.session_state.selected_card_index = (
            st.session_state.selected_card_index + 1
        ) % len(st.session_state.cards)
        st.rerun()

# -----------------------------
# 자료 표시
# -----------------------------
if show_resources:
    st.markdown("---")
    for res in card.get("resources", []):
        url = normalize_youtube_url(get_resource_url(card["id"], res))
        st.markdown(f"**{res['title']}**")
        if res["type"] == "video":
            st.video(url)
        elif res["type"] == "image":
            st.image(url, use_container_width=True)
