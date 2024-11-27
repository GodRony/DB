import streamlit as st
import hashlib

st.set_page_config(
    page_title="SQL Playground", 
    page_icon="✨"
    )

st.markdown("""
<style>
    #text_area_1 {
            background-color: #263238;
            color: #eeffff
}        
</style>
""",unsafe_allow_html=True)



# >>> DB연결

conn = st.connection('sqlite_db', type='sql')

@st.dialog("SQL 테이블")
def show_table_info():
    tables = ['course','takes','student']
    table_name = st.selectbox("테이블 선택", tables)
    # 테이블 내용 보기
    table = conn.query(f"SELECT * FROM {table_name} LIMIT 3;")
    st.write(table)

st.title = "SQL Playground"

if st.button("테이블 확인하기", type="primary"):
    # 드랍다운 메뉴로 만들기
    show_table_info()

def hash_answer(answer):
    return hashlib.sha256(str(answer).lower().strip().encode()).hexdigest()


# 코드 추가 >>>

col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("SQL 쿼리")
    query_form = st.form(key="query_form")
    raw_query = query_form.text_area("SQL쿼리를 입력하세요.", height=200)
    submit_btn = query_form.form_submit_button("실행")

with col2:
    st.header("SQL 결과")
    if submit_btn: # 버튼이 눌렸을 때   
        if raw_query == "":
            st.warning("SQL 쿼리를 입력하세요.")
            st.stop()     
        st.code(raw_query, language="sql")
        try: 
            result = conn.query(raw_query)
            st.dataframe(result)
        except Exception as e:
            st.error(f"오류 발생: {e}")
##
st.divider()


def check_answer(user_answer, key):
    hashed_answer = hash_answer(user_answer)
    gold_result= conn.query(f'SELECT answer FROM quiz_answer WHERE quiz_id = "{key}";')
    gold_answer = gold_result.iloc[0,0]
    return hashed_answer == gold_answer


with st.container():
    # 퀴즈 만들기
    st.header("SQL 퀴즈")
    st.write("1. Comp. Sci. 학과에서 가장 높은 총 학점(tot_cred)을 가진 학생의 이름은?")
    answer1 = st.text_input("답 1:")
    if st.button("확인",key="b1"):
        if check_answer(answer1, "q1"):
            st.success("정답입니다.")
        else:
            st.error("틀렸습니다.")

    st.write("2. 2017년 Fall 학기에 CS-101 과목을 수강한(takes) 학생은 몇 명인가?")
    answer2 = st.text_input("답 2:")
    if st.button("확인",key="b2"):
        if check_answer(answer2, "q2"):
            st.success("정답입니다.")
        else:
            st.error("틀렸습니다.")
    st.write("3. 가장 적은 학생들이 수강(takes)하는 과목(course)의 제목(title)은?")
    answer3 = st.text_input("답 3:")
    if st.button("확인",key="b3"):
        if check_answer(answer3, "q3"):
            st.success("정답입니다.")
        else:
            st.error("틀렸습니다.")
