import streamlit as st
import streamlit.components.v1 as components

from corse7_optimizer import process_excel as process7
from corse8_optimizer import process_excel as process8


# =====================================================
# 제목
# =====================================================

st.title("AI 집배순로 최적화 시스템")


# =====================================================
# 알고리즘 선택
# =====================================================

algorithm = st.radio(
    "최적화 방식 선택",
    [
        "corse7 - 통상순로 최적화",
        "corse8 - 통상순로 + 통상코스 최적화"
    ]
)


# =====================================================
# 파일 업로드
# =====================================================

uploaded_file = st.file_uploader(
    "엑셀 파일 업로드",
    type=["xlsx"]
)


# =====================================================
# 실행
# =====================================================

if uploaded_file is not None:

    st.success("엑셀 업로드 완료")

    if st.button("최적화 실행"):

        with st.spinner("AI 최적화 진행중..."):

            # =========================================
            # corse7 실행
            # =========================================

            if algorithm.startswith("corse7"):

                result = process7(uploaded_file)

            # =========================================
            # corse8 실행
            # =========================================

            else:

                result = process8(uploaded_file)

        st.success("최적화 완료")


        # =============================================
        # 결과 출력
        # =============================================

        st.subheader("요약 결과")

        st.dataframe(result["summary"])

        # =================================================
        # 비교지도
        # =================================================

        st.subheader("지도 비교")


        # =====================================================
        # 코스 탭
        # =====================================================

        course_count = len(result.get("compare_maps", []))

        # 지도 없을 때
        if course_count == 0:

            st.warning("생성된 비교지도가 없습니다.")

            st.write("result:")
            st.write(result)

        # 지도 있을 때만 tabs 생성
        else:

            course_tabs = st.tabs(
                [f"코스{i+1}" for i in range(course_count)]
            )

            # =====================================================
            # 코스별 지도 표시
            # =====================================================

            # =================================================
            # 지도 비교
            # =================================================

            st.subheader("지도 비교")

            if len(result.get("compare_maps", [])) == 0:

                st.warning("생성된 지도가 없습니다.")

            else:

                map_tabs = st.tabs(
                    ["원본", "최적화", "비교"]
                )

                # 원본지도
                with map_tabs[0]:

                    with open(
                        result["original_maps"][0],
                        "r",
                        encoding="utf-8"
                    ) as f:

                        map_html = f.read()

                    components.html(
                        map_html,
                        height=800
                    )

                # 최적화지도
                with map_tabs[1]:

                    with open(
                        result["optimized_maps"][0],
                        "r",
                        encoding="utf-8"
                    ) as f:

                        map_html = f.read()

                    components.html(
                        map_html,
                        height=800
                    )

                # 비교지도
                with map_tabs[2]:

                    with open(
                        result["compare_maps"][0],
                        "r",
                        encoding="utf-8"
                    ) as f:

                        map_html = f.read()

                    components.html(
                        map_html,
                        height=800
                    )

                                

                   
