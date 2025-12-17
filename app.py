import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="지구, 태양 주위를 떠도는 여정!",
    page_icon="🌍",
    layout="wide"
)


# -----------------------------
# 헬퍼 함수들
# -----------------------------
def has_distance_misconception(answer: str) -> bool:
    """거리/가까워서/멀어서와 관련된 오개념이 있는지 확인."""
    if not answer:
        return False
    keywords = ["거리", "가까워서", "가까워", "멀어서", "멀어", "가까운", "먼"]
    return any(k in answer for k in keywords)


def render_distance_feedback():
    """계절이 태양과의 거리 때문이라는 오개념에 대한 공통 피드백."""
    st.markdown("#### 🔍 거리와 계절에 대한 생각 정리")
    st.write(
        "선생님이 보시기에, 학생이 **태양과 지구 사이의 거리**에 주목했다는 점은 아주 좋은 관찰이에요."
    )
    st.write(
        "하지만 실제로는, 지구가 태양을 도는 동안 지구와 태양 사이의 거리는 **생각만큼 크게 달라지지 않기 때문에**, "
        "거리만으로는 여름과 겨울처럼 큰 계절 차이를 설명하기가 어렵습니다."
    )
    st.write(
        "계절이 생기는 더 중요한 이유는 **지구의 자전축이 약 23.5도 기울어져 있고**, "
        "그 기울어진 채로 **태양 주위를 공전하기 때문**이에요. "
        "그래서 같은 곳이라도 어떤 계절에는 태양빛이 더 수직에 가깝게, 어떤 계절에는 더 비스듬히 들어오게 됩니다."
    )


def render_auto_observe_block():
    """① 관찰 발문 전용 블록 - 질문 → 학생 답 → 자동 피드백."""
    st.subheader("① 관찰 발문")
    st.caption("수업 도입에서, 학생들이 이미 알고 있다고 생각하는 내용을 편안하게 말해 보도록 돕는 단계입니다.")

    # 메인 질문
    st.markdown("**계절이 변하는 까닭은 무엇일까요?**")

    answer = st.text_area(
        "학생 대답 입력창",
        key="observe_auto_answer",
        height=80,
        placeholder="학생이 실제로 말한 내용을 그대로 적어 두시면 좋습니다.",
    )

    if not answer:
        st.info("학생이 대답한 내용을 적어 주시면, 바로 아래에 피드백 문장이 자동으로 제안됩니다.")
        return

    st.markdown("----")
    st.markdown("#### 💬 자동 피드백 제안")

    # 1) 학생 대답을 존중하는 문장
    st.write(
        f"\"{answer}\"라고 생각해 주었군요. 계절이 왜 바뀌는지 스스로 이유를 떠올려 본 점이 정말 훌륭합니다."
    )

    # 2) 과학적으로 보완해 주는 설명
    st.write(
        "계절이 변하는 가장 큰 까닭은 **지구의 자전축이 약 23.5도 기울어진 채로 태양 주위를 공전하기 때문**이에요."
    )
    st.write(
        "이렇게 기울어진 지구가 공전하면서, 어떤 때에는 우리나라 쪽으로 태양빛이 더 정면에 가깝게 들어오고, "
        "어떤 때에는 더 비스듬히 들어오게 됩니다."
    )
    st.write(
        "그래서 같은 곳에서도 어떤 계절에는 햇빛이 강하고 낮이 길게 느껴지고, 다른 계절에는 햇빛이 약하고 밤이 길게 느껴지는 거예요."
    )

    # 3) 오개념(거리) 관련 추가 피드백
    if has_distance_misconception(answer):
        st.info("학생의 대답에 ‘거리’와 관련된 생각이 담겨 있는 것 같아요. 아래 내용을 함께 설명해 주세요.")
        render_distance_feedback()


def render_question_block(
    step_title: str,
    question: str,
    description: str,
    key_prefix: str,
    extra_feedback_lines: list[str],
    extra_materials: list[dict],
):
    """발문 1개, 학생 대답 입력, 피드백/추가 자료 버튼을 하나의 블록으로 렌더링."""
    st.subheader(step_title)
    if description:
        st.caption(description)

    st.markdown(f"**{question}**")

    answer = st.text_area(
        "학생 대답 입력창",
        key=f"{key_prefix}_answer",
        height=80,
        placeholder="학생이 실제로 말한 내용을 적어 두시면 좋습니다.",
    )

    col_feedback, col_material = st.columns(2)

    with col_feedback:
        show_feedback = st.button("피드백 보기", key=f"{key_prefix}_feedback_btn")
    with col_material:
        show_material = st.button("추가 자료 보기", key=f"{key_prefix}_material_btn")

    # 피드백 영역
    if show_feedback:
        st.markdown("----")
        st.markdown("#### 💬 피드백 제안")

        if answer:
            # 1) 학생 대답을 그대로 존중하는 1문장
            st.write(
                f"\"{answer}\"라고 생각해 주었군요. 이렇게 스스로 이유를 떠올려 보는 모습이 정말 좋습니다."
            )
        else:
            st.write("학생의 대답을 들은 뒤, 그 내용을 간단히 정리해 적어 두시면 좋습니다.")

        # 2) 과학적으로 보완해 주는 설명 (단계별 기본 피드백)
        for line in extra_feedback_lines:
            st.write(line)

        # 3) 오개념(거리) 관련 추가 피드백
        if has_distance_misconception(answer):
            st.info("학생의 대답에 ‘거리’ 개념이 포함된 것 같아요. 아래 내용을 함께 설명해 주세요.")
            render_distance_feedback()

    # 추가 자료 영역
    if show_material:
        st.markdown("----")
        st.markdown("#### 📚 추가 자료")
        for mat in extra_materials:
            st.markdown(f"**{mat['title']}**")
            if "description" in mat and mat["description"]:
                st.write(mat["description"])
            if "url" in mat and mat["url"]:
                # 실제 수업에서는 아래 URL을 학교에서 허용된 이미지/영상 링크로 교체해 주세요.
                if mat.get("type") == "image":
                    st.image(mat["url"], caption=mat.get("caption", None), use_column_width=True)
                elif mat.get("type") == "video":
                    st.video(mat["url"])
                else:
                    st.markdown(f"[자료 보기]({mat['url']})")
            st.markdown("---")


# -----------------------------
# 메인 레이아웃
# -----------------------------

st.title("🌍 지구, 태양 주위를 떠도는 여정! ")
st.markdown(
    

)
st.markdown("---")

tab_qna, tab_summary = st.tabs(["발문 중심 수업 보조", "한 장 정리"])


# -----------------------------
# 1) 발문 중심 수업 보조 탭
# -----------------------------
    # ① 관찰 발문 - 자동 피드백 버전
    render_auto_observe_block()

    st.markdown("---")

    # ② 추론 발문
    render_question_block(
        step_title="② 추론 발문",
        question="왜 여름에는 태양빛이 더 강하게 느껴질까요?",
        description="관찰한 내용을 바탕으로, 학생들이 스스로 이유를 추론해 보도록 하는 단계입니다.",
        key_prefix="reason",
        extra_feedback_lines=[
            "여름에는 태양이 더 높이 떠 있기 때문에, **태양빛이 땅에 더 수직에 가깝게** 들어옵니다.",
            "빛이 수직에 가깝게 들어오면 **같은 양의 빛이 더 작은 곳에 모여** 비추게 되어, 더 강하고 뜨겁게 느껴집니다.",
            "반대로 겨울에는 태양이 낮게 떠서 빛이 **비스듬히 들어오고**, 같은 양의 빛이 **넓게 퍼져서** 더 약하게 느껴집니다.",
        ],
        extra_materials=[
            {
                "title": "수직/비스듬한 태양빛 비교 그림",
                "description": "같은 양의 햇빛이 수직으로 비출 때와 비스듬히 비출 때, 땅에 닿는 빛의 농도를 비교한 그림입니다.",
                "type": "image",
                "url": "https://example.com/sunlight-angle-comparison.png",
                "caption": "수직/비스듬한 햇빛에 따른 에너지 분포 (예시 이미지 URL)",
            }
        ],
    )

    st.markdown("---")

    # ③ 검증 발문
    render_question_block(
        step_title="③ 검증 발문",
        question="그렇다면 계절은 지구가 태양에 가까워지거나 멀어져서 생긴다고 말해도 될까요?",
        description="학생들이 떠올린 생각을 검증해 보고, 맞는 부분과 보완이 필요한 부분을 함께 정리하는 단계입니다.",
        key_prefix="verify",
        extra_feedback_lines=[
            "많은 친구들이 **지구와 태양 사이의 거리가 달라져서** 계절이 생긴다고 생각하지만, 실제로는 그렇지 않습니다.",
            "지구는 1년 동안 타원 궤도로 공전하지만, 그 차이만으로는 여름과 겨울처럼 큰 온도 차이가 생기기 어렵습니다.",
            "따라서 계절 변화의 핵심 이유는 **지구의 자전축 기울기와 공전**이라는 점을 강조해 주시면 좋습니다.",
        ],
        extra_materials=[
            {
                "title": "지구 공전 궤도와 거리 변화 그림",
                "description": "지구가 타원 궤도로 공전하지만, 거리가 크게 달라지지 않는다는 것을 보여 주는 그림입니다.",
                "type": "image",
                "url": "https://example.com/earth-orbit-distance.png",
                "caption": "지구 공전 궤도와 태양과의 거리 (예시 이미지 URL)",
            }
        ],
    )

    st.markdown("---")

    # ④ 개념 정리 발문
    render_question_block(
        step_title="④ 개념 정리 발문",
        question="이제 계절이 생기는 까닭을 한 문장으로 말해 볼까요?",
        description="지금까지의 대화를 바탕으로, 학생 스스로 핵심 개념을 정리하도록 돕는 단계입니다.",
        key_prefix="summary",
        extra_feedback_lines=[
            "학생이 말한 문장을 토대로, 꼭 들어가야 할 핵심 표현을 하나씩 보완해 주세요.",
            "예를 들어, \"**지구의 자전축이 기울어진 채로 태양 주위를 공전하기 때문에** 계절이 생긴다\"와 같이 정리할 수 있습니다.",
            "가능하다면 학생과 함께 중요한 단어(자전축, 기울기, 공전, 태양빛의 각도)를 칠판에 정리해 보시는 것도 좋습니다.",
        ],
        extra_materials=[
            {
                "title": "한 문장 개념 정리 카드",
                "description": "수업 마지막에 학생들과 함께 읽을 수 있는 개념 정리 문장을 카드처럼 보여 주세요.",
                "type": "image",
                "url": "https://example.com/season-summary-card.png",
                "caption": "계절이 생기는 까닭 요약 카드 (예시 이미지 URL)",
            }
        ],
    )


# -----------------------------
# 2) 한 장 정리 탭
# -----------------------------
with tab_summary:
    st.header("📄 한 장 정리")
    st.markdown(
        """
### 계절이 생기는 까닭 핵심 정리

- **지구의 자전축은 약 23.5도 기울어져** 있습니다.  
- 이 기울어진 상태로 지구가 **태양 주위를 1년에 한 바퀴 공전**합니다.  
- 그래서 어떤 때에는 우리나라 쪽이 태양을 더 정면으로 바라보고,  
  어떤 때에는 태양을 더 비스듬히 바라보게 됩니다.  
- 이 때문에 한 곳에서도 **태양의 높이(태양 고도)와 햇빛이 들어오는 각도**가 계절에 따라 달라집니다.  
- 태양빛이 더 **수직에 가깝게** 들어오면 여름처럼 더 **뜨겁고 낮이 길게** 느껴지고,  
  더 **비스듬히** 들어오면 겨울처럼 더 **선선하고 밤이 길게** 느껴집니다.
"""
    )

    st.markdown("---")

    st.markdown("### 수업 정리용 체크리스트")
    st.checkbox("여름과 겨울에 태양의 높이 차이를 설명할 수 있다.", key="chk_height")
    st.checkbox("빛이 수직/비스듬히 들어올 때의 차이를 설명할 수 있다.", key="chk_angle")
    st.checkbox("계절이 태양과의 거리 때문이라는 생각이 왜 정확하지 않은지 설명할 수 있다.", key="chk_distance")
    st.checkbox("자전축 기울기와 공전이 계절과 어떻게 연결되는지 말할 수 있다.", key="chk_tilt_orbit")

    st.markdown("---")
    st.markdown(
        """
### 선생님께 드리는 제안
- 이 탭은 학생들에게 그대로 읽어 주는 것보다는,  
  **수업이 끝날 무렵 선생님이 핵심을 다시 짚어 보실 때 참고 자료**로 활용해 주세요.
- 학생 스스로 말로 정리하게 한 뒤, 빠진 부분이 있을 때만 이 내용을 보완 자료로 사용하시면 좋습니다.
"""
    )
