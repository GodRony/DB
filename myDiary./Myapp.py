import streamlit as st
from sqlalchemy.sql import text

# DB 연결
conn = st.connection('mysql', type='sql')

df = conn.query('SELECT * FROM day LIMIT 5;', ttl=600)

# 타이틀
st.title('일기 및 일정관리 앱')


def diary_writing_page():
    st.subheader("일기작성")
    d = st.date_input(
        "날짜 입력",
        min_value = None,
        max_value= None
        )
    
    if st.button("날짜 입력 완료"):
        with conn.session as session:
            try:
                # SQL 쿼리 실행 (날짜와 사용자 ID를 INSERT)
                insert_query = text("""
                    INSERT INTO day (date, users_user_id)
                    VALUES (:date, :user_id)
                """)
                
                # 실행할 데이터 준비
                session.execute(insert_query, {"date": d, "user_id": 1})  # 예시로 user_id = 1로 설정
                
                # 커밋하여 변경 사항을 저장
                session.commit()
                
                # 성공 메시지
                st.success(f"{d} 날짜가 추가되었습니다.")
            except Exception as e:
                # 오류 발생 시 메시지 출력
                st.error(f"저장 중 오류가 발생했습니다: {str(e)}")

    category = st.selectbox("카테고리", ["가족일기", "그외일기", "반려동물일기"])
    mood = st.selectbox("기분", ["매우 나쁨", "나쁨", "보통", "좋음", "매우좋음"])
    st.write("포인트:", 1)
    memo = st.text_area("메모")
    photo = st.file_uploader("사진 업로드", type=["png", "jpg", "jpeg"])

    if st.button("일기 저장"):

        
        with conn.session as session:
            try:
                category_id = conn.query(
                    f"SELECT category_id FROM category "
                    f"WHERE category_name = '{category}'"
                ).iloc[0]['category_id']

                mood_id = conn.query(
                    f"SELECT mood_id FROM mood WHERE mood_name = '{mood}'"
                ).iloc[0]['mood_id']

                session.execute(
                    text("""
                        INSERT INTO diary (memo, category_category_id, mood_mood_id,day_date)
                        VALUES (:memo, :category_id, :mood_id, :current_date)
                    """),
                    {
                        "memo": memo,
                        "category_id": category_id,
                        "mood_id": mood_id,
                        "current_date": d
                    }
                )
                session.commit()
                st.success("일기가 저장되었습니다!")
            except Exception as e:
                st.error(f"저장 중 오류가 발생했습니다: {str(e)}")


def show_diaries():

    

    query = """
        SELECT
           d.diary_id,
           d.memo,
           d.category_category_id,
           d.mood_mood_id,
           d.day_date,
           u.name   
        FROM diary d
        JOIN day ON day.date = d.day_date  -- day 테이블과 diary 테이블을 day_id로 연결
        JOIN users u ON u.user_id = day.users_user_id  -- day 테이블과 users 테이블을 user_id로 연결


    """
        #     JOIN users u ON d.user_id = u.user_id
        # JOIN mood m ON d.mood_id = m.mood_id
        # ORDER BY d.created_at DESC;
    df = conn.query(query, ttl=0)

    for row in df.itertuples():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"{row.name} ")
            with col2:
                st.write(f"아이디 : {row.diary_id},  기분 포인트 :{row.mood_mood_id}")
                st.write(row.memo)
                st.write(f"작성일: {row.day_date.strftime('%Y-%m-%d %H:%M')}")
            st.divider()


def view_page():
    st.title("일기 보기")
    st.subheader("일기 삭제")
    diary_id_to_delete = st.text_input("삭제할 일기의 ID를 입력하세요:")

    if st.button("일기 삭제", type='primary'):
        if diary_id_to_delete.strip(): 
            try:
                diary_id = int(diary_id_to_delete)
                with conn.session as session:
                    delete_query = text(
                        "DELETE FROM diary WHERE diary_id = :diary_id"
                    )
                    result = session.execute(delete_query, {"diary_id": diary_id})
                    session.commit()

                    if result.rowcount > 0:
                        st.success("일기가 삭제되었습니다!")
                        st.rerun()
                    else:
                        st.warning("해당 ID의 일기를 찾을 수 없습니다.")
            except ValueError:
                st.error("올바른 숫자 형식의 ID를 입력해주세요.")
            except Exception as e:
                st.error(f"삭제 중 오류가 발생했습니다: {str(e)}")
    show_diaries()


# 페이지 선택
st.sidebar.title("페이지 선택")
page = st.sidebar.radio("이동할 페이지를 선택하세요", ["일기 작성", "일기 확인"])

if page == "일기 작성":
    diary_writing_page()
elif page == "일기 확인":
    view_page()
