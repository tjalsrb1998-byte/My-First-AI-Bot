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
    """config.json에서 자료 URL 설정을 불러옵니다."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("resource_urls", {})
        except Exception:
            return {}
    return {}


def save_resource_urls(resource_urls: Dict) -> None:
    """자료 URL 설정을 config.json에 저장합니다."""
    payload = {"resource_urls": resource_urls}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# -----------------------------
# 유튜브 링크 정규화 (Streamlit st.video 호환 우선)
# - embed URL 대신 watch URL을 사용 (st.video가 더 안정적으로 동작)
# -----------------------------
def normalize_youtube_url(url: str) -> str:
    """
    Streamlit st.video에서 잘 재생되도록 유튜브 URL을 watch 형태로 정규화합니다.
    지원:
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID
    - 공유 파라미터(?feature=share 등) 제거
    """
    if not url:
        return url

    u = url.strip()

    # youtu.be/<id>
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{6,})", u)
    if m:
        vid = m.group(1)
        return f"https://www.youtube.com/watch?v={vid}"

    # youtube.com/shorts/<id>
    m = re.search(r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})", u)
    if m:
        vid = m.group(1)
        return f"https://www.youtube.com/watch?v={vid}"

    # youtube.com/watch?v=<id>
    m = re.search(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})", u)
    if m:
        vid = m.group(1)
        return f"https://www.youtube.com/watch?v={vid}"

    # youtube.com/embed/<id>  -> watch로 변환 (선택)
    m = re.search(r"youtube\.com/embed/([A-Za-z0-9_-]{6,})", u)
    if m:
        vid = m.group(1)
        return f"https://www.youtube.com/watch?v={vid}"

    return u


def is_youtube_url(url: str) -> bool:
    if not url:
        return False
    u = url.lower()
    return ("youtube.com" in u) or ("youtu.be" in u)


# -----------------------------
# 발문 카드 데이터
# -----------------------------
def get_default_cards() -> List[Dict]:
    """수업에서 사용할 발문 카드를 정의합니다."""
    return [
        {
            "id": "obs_sun_appearance",
            "stage": "생각해보기",
            "label": "생각해보기: 계절 변화의 까닭",
            "question": "계절의 변화가 생기는 까닭은 무엇일까요?",
            "expected_answers": [
                "여름에는 태양이 더 높이 떠 있고, 겨울에는 낮게 떠요.",
                "여름에는 햇빛이 강고 눈이 부시고, 겨울에는 햇빛이 약하게 느껴져요.",
                "여름에는 하늘 가운데 쪽에서 비추고, 겨울에는 옆쪽에서 비추는 느낌이에요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "axis_tilt",
                    "title": "지구 자전축 23.5도 기울기 그림",
                    "type": "image",
                    "default_url": "https://blog.kakaocdn.net/dna/doM62b/btsJXYwTxbx/AAAAAAAAAAAAAAAAAAAAACkh66jHRVAuJuZUNXWiTpgXEoHXXbJvF-B--_urBXeo/img.webp?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1767193199&allow_ip=&allow_referer=&signature=HZ%2FEJBS2ZsxegP4O5C%2BUWi8coXg%3D",
                    "description": "지구가 자전축이 기울어진 채로 태양 주위를 도는 모습을 보여 주는 그림입니다.",
                },
                {
                    "id": "sun_height",
                    "title": "여름/겨울 태양 높이 비교 그림",
                    "type": "image",
                    "default_url": "https://www.home-learn.co.kr/common/image.do?imgPath=newsroom&imgName=CK20230202092852423.png&imgGubun=D",
                    "description": "같은 장소에서 여름과 겨울에 태양이 어느 높이까지 올라가는지 비교한 그림입니다.",
                },
            ],
            "teacher_notes": {
                "extra_questions": [
                    "여름과 겨울에 그림자 길이도 함께 떠올려 보면 어떤 차이가 있을까요?",
                    "태양이 뜨고 지는 위치도 계절마다 달라지는지 이야기해 볼까요?",
                ],
                "teacher_point": "학생들의 말 속에서 '태양 높이', '햇빛의 느낌', '그림자 길이' 같은 표현을 끌어내어, 나중에 태양 고도 개념으로 연결할 준비를 합니다.",
            },
        },
        {
            "id": "obs_shadow_length",
            "stage": "관찰",
            "label": "관찰: 그림자 길이",
            "question": "여름과 겨울에 같은 시간에 서 있으면, 그림자 길이는 어떻게 달라질까요?",
            "expected_answers": [
                "여름에는 그림자가 짧고, 겨울에는 그림자가 길어요.",
                "겨울에는 해가 낮게 있어서 그림자가 훨씬 길어져요.",
                "계절이 바뀔 때마다 놀이터에서 생기는 그림자 길이도 조금씩 달라져요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "shadow_compare",
                    "title": "여름/겨울 그림자 길이 비교 사진",
                    "type": "image",
                    "default_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNZU4uiSOMiiRvWfPsNhQoPCLbDg2PR-8NQg&s",
                    "description": "같은 시간에 찍은 여름과 겨울의 그림자 길이를 비교한 사진입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "그림자가 길다는 것은 태양이 하늘에서 어느 쪽에 있다는 뜻일까요?",
                    "그림자 길이와 태양 높이는 어떤 관계가 있을지 스스로 말해 보게 해 주세요.",
                ],
                "teacher_point": "그림자 길이 경험을 통해 태양 고도가 낮을수록 그림자가 길어진다는 직관을 쌓게 합니다.",
            },
        },
        {
            "id": "obs_day_length",
            "stage": "관찰",
            "label": "관찰: 낮의 길이",
            "question": "낮의 길이는 계절에 따라 어떻게 달라질까요?",
            "expected_answers": [
                "여름에는 낮이 길고 밤이 짧아요.",
                "겨울에는 낮이 짧고 밤이 길어요.",
                "봄과 가을은 여름과 겨울의 중간 정도 길이라고 느껴져요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "daylength_chart",
                    "title": "계절에 따른 낮 길이 변화 그래프",
                    "type": "image",
                    "default_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHNbhrKiUFY1Q82K_M1_SBajnuuaS-tRaN1A&s",
                    "description": "계절에 따라 낮 시간이 어떻게 길어졌다가 짧아지는지 보여 주는 그래프입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "학생들이 실제로 느끼는 '해가 빨리 진다/늦게 진다' 경험을 떠올리게 해 주세요.",
                    "하루 동안 태양이 떠 있는 시간이 길어지면 기온에는 어떤 영향을 줄지 함께 이야기해 보세요.",
                ],
                "teacher_point": "낮과 밤의 길이 변화를 자전축 기울기와 공전과 연결하기 위한 기초 경험을 확인합니다.",
            },
        },
        {
            "id": "reason_sunlight",
            "stage": "생각해보기",
            "label": "생각해보기: 햇빛이 더 강하게 느껴지는 까닭",
            "question": "왜 여름에는 햇빛이 더 강하게 느껴질까요?",
            "expected_answers": [
                "여름에는 태양이 높이 떠 있어서 햇빛이 더 세게 내려와요.",
                "햇빛이 더 위에서 바로 내려와서 같은 곳에 더 많이 모여요.",
                "여름에는 태양빛이 거의 바로 내려와서 그림자도 짧게 보여요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "angle_energy",
                    "title": "수직/비스듬한 햇빛과 에너지 분포 그림",
                    "type": "image",
                    "default_url": "https://mblogthumb-phinf.pstatic.net/20121024_208/msy879_1351057881359nbj8s_JPEG/%C0%A7%B5%B5%BA%B0_%C5%C2%BE%E7%BA%B9%BB%E7%BF%A1%B3%CA%C1%F6.jpg?type=w420",
                    "description": "같은 양의 햇빛이 수직으로 들어올 때와 비스듬히 들어올 때, 단위 면적에 도달하는 에너지 차이를 보여 주는 그림입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "손전등을 책상에 비출 때, 바로 위에서 비출 때와 비스듬히 비출 때의 밝기는 어떻게 다른가요?",
                    "같은 양의 빛이 더 작은 곳에 모이면 어떻게 느껴질지 학생이 말해 보게 해 주세요.",
                ],
                "teacher_point": "빛의 입사각과 단위 면적당 에너지 양을 연결하여, 단순히 '여름이니까 뜨겁다'가 아니라 '빛의 각도'로 사고하게 돕습니다.",
            },
        },
        {
            "id": "reason_oblique",
            "stage": "생각해보기",
            "label": "생각해보기: 비스듬한 햇빛",
            "question": "햇빛이 비스듬히 들어오면 어떤 일이 생길까요?",
            "expected_answers": [
                "빛이 넓게 퍼져서 한 곳에 도달하는 양이 줄어들 것 같아요.",
                "같은 양의 빛이라도 비스듬히 들어오면 덜 뜨겁게 느껴질 거예요.",
                "그림자가 길어지고, 땅이 덜 데워질 것 같다고 느껴요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "flashlight_demo",
                    "title": "손전등 비스듬히 비추기 실험(자료 링크)",
                    "type": "image",
                    "default_url": "https://cloudfront-ap-northeast-1.images.arcpublishing.com/chosun/MUXVC2EQKDKWZF7FIZCP36AWGY.jpg",
                    "description": "손전등을 수직/비스듬히 비출 때 빛이 퍼지는 모습을 비교하는 자료입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "종이에 손전등을 수직/비스듬히 비춰 보면서 밝기 차이를 실제로 관찰해 보게 하세요.",
                    "이 실험 결과를 계절이 바뀌는 이유와 어떻게 연결할 수 있을지 학생에게 먼저 말해 보게 해 주세요.",
                ],
                "teacher_point": "‘빛이 퍼지면 힘이 약해진다’는 직관을 만들도록 돕습니다.",
            },
        },
        {
            "id": "misconception_distance",
            "stage": "더 생각해보기",
            "label": "더 생각해보기: 거리 오개념 확인",
            "question": "계절은 지구가 태양에 가까워져서 또는 멀어져서 생긴다고 말해도 될까요?",
            "expected_answers": [
                "가까워서 덥고, 멀어서 추운 거라고 생각했어요.",
                "조금은 거리도 관계가 있을 것 같은데, 그것만으로는 설명이 안 되는 것 같아요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "orbit_shape",
                    "title": "지구 공전 궤도와 거리 변화 그림",
                    "type": "image",
                    "default_url": "https://flexible.img.hani.co.kr/flexible/normal/800/453/imgdb/original/2025/0104/20250104500223.jpg",
                    "description": "지구가 타원 궤도로 돌지만, 거리 차이는 계절을 설명하기엔 크지 않다는 점을 보여 주는 자료입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "만약 거리가 정말 크게 달라진다면, 봄과 가을의 온도는 어떻게 되어야 할까요?",
                    "우리나라가 겨울일 때, 지구의 다른 지역은 어떤 계절인지 함께 생각해 보게 해 주세요.",
                ],
                "teacher_point": "거리 오개념을 바로 ‘틀렸다’고 말하기보다, 거리만으로는 설명이 어려운 사례를 떠올리게 합니다.",
            },
        },
        {
            "id": "elab_tilt",
            "stage": "더 생각해보기",
            "label": "더 생각해보기: 자전축 기울기 의미",
            "question": "‘지구의 자전축이 기울어져 있다’는 말은 어떤 뜻일까요?",
            "expected_answers": [
                "지구가 세워져서 도는 게 아니라 약간 기울어진 채로 돌고 있어요.",
                "연필을 약간 비스듬히 세워서 돌리는 것처럼, 지구도 기울어진 채로 태양 주위를 돌아요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "tilt_demo",
                    "title": "자전축 기울기 모형",
                    "type": "image",  # ✅ '영상'이면 video 권장
                    # ⚠️ proxy 류 URL은 자주 깨집니다. 가능하면 유튜브/공개 mp4 링크로 교체하세요.
                    "default_url": "https://lh3.googleusercontent.com/proxy/nclZ50T2eiYfpsAxGXmzSUULp13EOThsLQNUpHF7Ar-SlrHFeg3QcXngPHuRUUsQScX5R8LcdEgZahim96CakSngDtHqqPU",
                    "description": "자전축 기울기 모형을 보여주는 이미지입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "자전축이 기울어진 채로 태양 주위를 돈다면, 어느 쪽 반구가 더 햇빛을 많이 받을까요?",
                    "기울기가 없다면 계절은 어떻게 될지 상상해 보게 해 주세요.",
                ],
                "teacher_point": "‘기울어짐’과 ‘공전’을 함께 언급하여, 자전축 기울기가 계절과 어떻게 연결되는지 정교화합니다.",
            },
        },
        {
            "id": "summary_sentence",
            "stage": "정리",
            "label": "정리: 한 문장으로 계절 설명",
            "question": "계절이 생기는 까닭을 한 문장으로 말해 볼까요?",
            "expected_answers": [
                "지구의 자전축이 기울어진 채로 태양 주위를 공전하기 때문에 계절이 생겨요.",
                "지구가 기울어진 채로 도는 동안 태양빛이 비추는 각도와 낮의 길이가 달라져서 계절이 생겨요.",
            ],
            "feedback_rules": {},
            "resources": [
                {
                    "id": "summary_card",
                    "title": "계절 개념 총정리 영상",
                    "type": "image",
                    "default_url": "https://www.home-learn.co.kr/common/image.do?imgPath=newsroom&imgName=CK20230202093400748.png&imgGubun=D",
                    "description": "수업 최종 정리용 계절 개념 요약 이미지입니다.",
                }
            ],
            "teacher_notes": {
                "extra_questions": [
                    "방금 말해 준 문장에서 꼭 들어가야 한다고 생각하는 단어를 밑줄 그어 볼까요? (예: 자전축, 기울기, 공전)",
                    "친구에게 설명하듯이, 조금 더 쉽게 풀어서 다시 말해 볼 수 있을까요?",
                ],
                "teacher_point": "학생이 만든 문장을 존중하고, 빠진 핵심어(자전축, 기울기, 공전, 태양빛 각도)를 하나씩 보완해 줍니다.",
            },
        },
    ]


# -----------------------------
# 피드백 규칙 엔진
# -----------------------------
def classify_answer(answer: str) -> str:
    """학생 답변을 간단한 키워드 기반으로 분류합니다."""
    if not answer or not answer.strip():
        return "empty"

    text = answer.replace(" ", "").lower()

    distance_keywords = ["거리", "가까워", "가까워서", "멀어", "멀어서", "distance"]
    tilt_keywords = ["자전축", "기울", "23.5", "23도", "축이기울어", "axis", "tilt"]
    angle_keywords = ["각도", "비스듬", "수직", "남중고도", "태양고도", "높이"]
    daylength_keywords = ["낮이", "밤이", "낮길이", "밤길이", "낮과밤", "해가길게", "해가짧게"]

    if any(k in text for k in distance_keywords):
        return "distance"
    if any(k in text for k in tilt_keywords):
        return "tilt"
    if any(k in text for k in angle_keywords):
        return "angle"
    if any(k in text for k in daylength_keywords):
        return "daylength"

    return "other"


def build_feedback(answer: str, card: Dict) -> str:
    """
    규칙 기반으로 피드백 문단을 생성합니다.
    형식: 결론 1문장 + 보완 2~3문장 + 확인 질문 1개
    """
    category = classify_answer(answer)

    if answer and answer.strip():
        head = f"“{answer}”라고 생각해 주신 점이 정말 좋습니다. 스스로 계절이 생기는 까닭을 고민해 본 것만으로도 큰 배움이에요."
    else:
        head = "아직 생각을 적지 않았네요. 떠오르는 생각을 편하게 한 문장이라도 적어 보면 좋겠습니다."

    lines: List[str] = [head]

    if category == "distance":
        lines.append("태양과 지구 사이의 거리를 떠올린 것은 아주 자연스러운 생각이에요. 멀어지면 추워지고 가까워지면 더워질 것 같다고 느끼기 쉽지요.")
        lines.append("하지만 실제로는 지구가 1년 동안 태양을 도는 동안 **거리 차이는 그리 크지 않아서**, 여름과 겨울처럼 큰 온도 차이를 만들 만큼의 이유가 되지는 않습니다.")
        lines.append("계절이 생기는 더 중요한 까닭은 **지구의 자전축이 기울어진 채로 태양 주위를 공전하면서**, 태양빛이 비추는 각도와 낮의 길이가 달라지기 때문이에요.")
        lines.append("그렇다면 만약 거리가 계절의 주된 이유라면, 지구가 태양에서 가장 멀어질 때 우리나라에는 어떤 계절이 와야 할지 함께 다시 생각해 볼까요?")

    elif category == "tilt":
        lines.append("자전축이 기울어져 있다는 말을 해 주신 것은 아주 중요한 핵심을 잘 짚은 거예요. 계절의 비밀에 거의 다가간 셈입니다.")
        lines.append("지구의 자전축이 약 23.5도 기울어진 채로 **태양 주위를 공전**하기 때문에, 어떤 때에는 우리나라 쪽이 태양을 더 정면으로 바라보고, 어떤 때에는 더 비스듬히 바라보게 됩니다.")
        lines.append("그래서 계절마다 태양빛이 비추는 각도와 낮의 길이가 달라지고, 그 결과로 여름과 겨울 같은 계절 차이가 나타나게 돼요.")
        lines.append("지금 이야기한 자전축 기울기와 공전을 한 문장 안에 넣어서, “그래서 계절이 생긴다”까지 이어서 다시 설명해 볼 수 있을까요?")

    elif category == "angle":
        lines.append("햇빛이 **수직에 가깝게** 혹은 **비스듬히** 들어온다는 점을 떠올린 것은 과학적으로 매우 예리한 관찰이에요.")
        lines.append("같은 양의 햇빛이라도 수직에 가깝게 들어오면 **작은 면적에 에너지가 모여서** 더 뜨겁게 느껴지고, 비스듬히 들어오면 **넓은 면적에 퍼져서** 약하게 느껴집니다.")
        lines.append("즉, 빛이 비스듬히 들어올수록 단위 면적당 받는 에너지가 줄어드는 셈이에요.")
        lines.append("그렇다면 겨울에는 왜 여름보다 햇빛이 덜 강하게 느껴지는지, ‘각도’라는 말을 넣어서 다시 말해 볼까요?")

    elif category == "daylength":
        lines.append("낮의 길이와 밤의 길이를 떠올린 것은 계절을 이해하는 데 아주 중요한 관찰이에요.")
        lines.append("지구의 자전축이 기울어진 채로 태양 주위를 공전하면서, 어떤 때에는 우리나라가 태양을 더 오래 바라보게 되어 **낮이 길어지고**, 어떤 때에는 덜 오래 바라보게 되어 **밤이 길어지게** 됩니다.")
        lines.append("그래서 낮이 길어질수록 여름처럼 더 따뜻하게 느껴지고, 낮이 짧아질수록 겨울처럼 더 선선하게 느껴질 수 있어요.")
        lines.append("방금 이야기한 ‘낮 길이 변화’를 자전축 기울기와 공전이라는 말까지 넣어서 한 문장으로 정리해 볼 수 있을까요?")

    elif category == "other":
        lines.append("지금 적어 주신 생각 속에도 분명 중요한 단서들이 숨어 있어요. 아직은 조금 막연하게 느껴질 수 있습니다.")
        lines.append("조금 더 구체적으로, **태양의 높이**, **햇빛이 비추는 각도**, **낮과 밤의 길이** 중에서 무엇과 가장 관련이 있을지 하나를 골라서 다시 설명해 보면 좋아요.")
        lines.append("“어떤 계절에는 태양이 어떻게 보이고, 그래서 무엇이 달라진다”처럼 문장을 한 번 더 만들어 볼까요?")

    else:  # empty
        lines.append("처음부터 완벽한 답을 쓰려고 하기보다, 떠오르는 단어 두세 개만 적어 보는 것도 좋은 시작입니다.")
        lines.append("예를 들어 ‘태양빛의 각도’, ‘자전축 기울기’, ‘낮의 길이’처럼 계절과 관련이 있을 것 같은 말을 하나 골라 적어 보세요.")
        lines.append("이 중에서 어떤 단어가 계절과 가장 깊은 관련이 있을지, 다음 차례에 말로 설명해 볼 수 있을까요?")

    return "\n\n".join(lines)


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "cards" not in st.session_state:
    st.session_state.cards = get_default_cards()

if "resource_urls" not in st.session_state:
    st.session_state.resource_urls = load_resource_urls()

if "selected_card_index" not in st.session_state:
    st.session_state.selected_card_index = 0

# 버튼 눌렀을 때 상태 유지용
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "show_resources" not in st.session_state:
    st.session_state.show_resources = False


def get_cards() -> List[Dict]:
    return st.session_state.cards


def get_resource_url(card_id: str, res: Dict) -> str:
    card_urls = st.session_state.resource_urls.setdefault(card_id, {})
    return card_urls.get(res["id"], res.get("default_url", ""))


def set_resource_url(card_id: str, res_id: str, url: str) -> None:
    card_urls = st.session_state.resource_urls.setdefault(card_id, {})
    card_urls[res_id] = url


def render_resource(res: Dict, url: str) -> None:
    """리소스 타입을 우선으로 안전하게 렌더링합니다."""
    rtype = (res.get("type") or "").lower()

    # 항상 링크도 함께 제공(차단/만료 URL 원인 파악용)
    if url:
        st.caption(f"링크: {url}")

    if not url:
        st.info("URL이 비어 있습니다. 사이드바에서 주소를 입력해 주세요.")
        return

    # video 우선 처리
    if rtype == "video":
        if is_youtube_url(url):
            st.video(normalize_youtube_url(url))
        else:
            st.video(url)
        return

    # image 처리
    if rtype == "image":
        st.image(url, use_container_width=True)
        return

    # 기타
    st.markdown(f"[자료 열기]({url})")


# -----------------------------
# 레이아웃: 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 수업 설정")

    cards = get_cards()
    labels = [f"[{c['stage']}] {c['label']}" for c in cards]

    selected_index = st.selectbox(
        "사용할 발문 카드를 선택하세요.",
        options=list(range(len(labels))),
        format_func=lambda i: labels[i],
        index=st.session_state.selected_card_index,
    )
    st.session_state.selected_card_index = selected_index
    current_card = cards[selected_index]

    st.markdown("---")
    st.subheader("📎 자료 링크 설정")
    st.caption("학교에서 사용 가능한 이미지/영상 URL로 바꾸어 사용하실 수 있습니다.")

    for res in current_card.get("resources", []):
        current_url = get_resource_url(current_card["id"], res)
        new_url = st.text_input(
            f"{res['title']} URL",
            value=current_url,
            key=f"url_{current_card['id']}_{res['id']}",
        )
        set_resource_url(current_card["id"], res["id"], new_url)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 자료 링크 저장", use_container_width=True):
            save_resource_urls(st.session_state.resource_urls)
            st.success("저장되었습니다! (config.json)")
    with col_b:
        if st.button("🧹 초기화", use_container_width=True):
            st.session_state.resource_urls = {}
            save_resource_urls(st.session_state.resource_urls)
            st.warning("초기화되었습니다. 기본 URL로 다시 시작합니다.")

    st.caption("※ 저장 후 새로고침해도 유지됩니다.")


# -----------------------------
# 메인 레이아웃
# -----------------------------
st.title("🌍 지구, 태양 주위를 떠도는 여정")
st.markdown("---")

tab_lesson, tab_summary = st.tabs(["발문 카드 활용", "한 장 정리"])


# -----------------------------
# 탭 1: 발문 카드 활용
# -----------------------------
with tab_lesson:
    cards = get_cards()
    current_index = st.session_state.selected_card_index
    card = cards[current_index]

    st.markdown(f"#### 단계: {card['stage']}")
    st.markdown(f"**{card['question']}**")

    st.markdown("##### 학생 답 입력")
    # ✅ 문구 숨김: label="" + label_visibility="collapsed"
    answer = st.text_area(
        label="",
        key=f"answer_{card['id']}",
        height=100,
        placeholder="예) 여름에는 태양이 가까워져서 더워지고, 겨울에는 멀어져서 추워진 것 같아요.",
        label_visibility="collapsed",
    )

    # ✅ 버튼: 동일 폭/간격 + 원하는 순서
    col_prev, col_fb, col_res, col_next = st.columns(4)

    with col_prev:
        prev_clicked = st.button("이전 단계로 돌아가기", key=f"prev_btn_{card['id']}", use_container_width=True)
    with col_fb:
        fb_clicked = st.button("피드백 보기", key=f"fb_btn_{card['id']}", use_container_width=True)
    with col_res:
        res_clicked = st.button("추가 자료 보기", key=f"res_btn_{card['id']}", use_container_width=True)
    with col_next:
        next_clicked = st.button("다음 단계로 넘어가기", key=f"next_btn_{card['id']}", use_container_width=True)

    # 클릭 상태 반영(토글)
    if fb_clicked:
        st.session_state.show_feedback = True
        st.session_state.show_resources = False
    if res_clicked:
        st.session_state.show_resources = True
        st.session_state.show_feedback = False

    if prev_clicked:
        st.session_state.selected_card_index = (current_index - 1) % len(cards)
        st.session_state.show_feedback = False
        st.session_state.show_resources = False
        st.rerun()

    if next_clicked:
        st.session_state.selected_card_index = (current_index + 1) % len(cards)
        st.session_state.show_feedback = False
        st.session_state.show_resources = False
        st.rerun()

    if st.session_state.show_feedback:
        st.markdown("---")
        st.subheader("💬 규칙 기반 피드백")
        st.write(build_feedback(answer, card))

    if st.session_state.show_resources:
        st.markdown("---")
        st.subheader("📚 추가 자료")
        resources = card.get("resources", [])
        if not resources:
            st.info("이 카드에 등록된 자료가 아직 없습니다. 사이드바에서 URL을 추가해 보세요.")
        else:
            for res in resources:
                url = get_resource_url(card["id"], res)
                st.markdown(f"**{res.get('title', '자료')}**")
                if res.get("description"):
                    st.caption(res["description"])
                render_resource(res, url)
                st.markdown("---")


# -----------------------------
# 탭 2: 한 장 정리
# -----------------------------
with tab_summary:
    st.header("📄 계절이 생기는 까닭 - 한 장 정리")
    st.markdown(
        """
- 지구의 **자전축은 약 23.5도 기울어져** 있습니다.  
- 이 기울어진 상태로 지구가 **태양 주위를 1년에 한 바퀴 공전**합니다.  
- 그래서 어떤 때에는 우리나라 쪽이 태양을 더 정면으로 바라보고, 어떤 때에는 더 비스듬히 바라보게 됩니다.  
- 그 결과, 한 장소에서도 **태양의 높이(태양 고도)** 와 **햇빛이 비추는 각도**, **낮과 밤의 길이**가 계절에 따라 달라집니다.  
- 태양빛이 더 **수직에 가깝게** 들어오고 낮이 길어질수록 여름처럼 더 **뜨겁고 밝게**,  
  더 **비스듬히** 들어오고 낮이 짧아질수록 겨울처럼 더 **선선하고 어둡게** 느껴집니다.
"""
    )

    st.markdown("---")
    st.markdown("### 수업 마무리 체크리스트")
    st.checkbox("여름과 겨울에 태양의 높이와 그림자 길이 차이를 설명할 수 있다.", key="chk_sun_height")
    st.checkbox("햇빛의 입사각(수직/비스듬히)과 단위 면적당 에너지 양의 관계를 말할 수 있다.", key="chk_angle_energy")
    st.checkbox("계절이 태양과의 거리 때문이라는 생각이 왜 정확하지 않은지 설명할 수 있다.", key="chk_distance_misconception")
    st.checkbox("자전축 기울기와 공전이 계절과 어떻게 연결되는지 한 문장으로 말할 수 있다.", key="chk_tilt_orbit")

    st.markdown("---")
