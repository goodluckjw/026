import streamlit as st
from processing.law_processor import get_law_list_from_api, get_highlighted_articles

st.title("📘 부칙 개정 도우미 (정렬 + 상세조문 확인)")

search_word = st.text_input("🔍 찾을 단어", placeholder="예: 지방법원")
sort_alpha = st.checkbox("🔠 법령명 가나다순 정렬", value=True)
filter_keyword = st.text_input("🧹 법령명 필터링 (선택)", placeholder="예: 민법")

if st.button("🚀 시작하기"):
    if not search_word:
        st.warning("찾을 단어를 입력해주세요.")
    else:
        with st.spinner("법령 검색 중..."):
            laws = get_law_list_from_api(search_word)
            if filter_keyword:
                laws = [law for law in laws if filter_keyword in law['법령명']]
            if sort_alpha:
                laws = sorted(laws, key=lambda x: x['법령명'])

            st.success(f"✅ 총 {len(laws)}개의 법령을 찾았습니다.")

            for law in laws:
                with st.expander(f"📘 {law['법령명']} [+]", expanded=False):
                    st.markdown(f"[🔗 법령 보기]({law['URL']})", unsafe_allow_html=True)
                    article_text = get_highlighted_articles(law['MST'], search_word)
                    st.markdown(article_text, unsafe_allow_html=True)
