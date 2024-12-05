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
    st.subheader("일기 확인 및 삭제")
    
    # 삭제할 일기 ID 입력
    diary_id_to_delete = st.text_input("삭제할 일기의 ID를 입력하세요:")

    if st.button("일기 삭제", type="primary"):
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
                        st.experimental_rerun()  # 페이지 새로고침
                    else:
                        st.warning("해당 ID의 일기를 찾을 수 없습니다.")
            except ValueError:
                st.error("올바른 숫자 형식의 ID를 입력해주세요.")
            except Exception as e:
                st.error(f"삭제 중 오류가 발생했습니다: {str(e)}")

    # 기본적으로 모든 일기 보여주기
    st.subheader("모든 일기 확인")
    show_diaries()

    # 날짜별 일기 확인
    st.subheader("날짜별 일기 확인")
    selected_date = st.date_input("확인할 날짜를 입력하세요:")

    if st.button("날짜로 일기 확인"):
        with conn.session as session:
            try:
                # 특정 날짜의 다이어리 데이터를 가져오는 SQL 쿼리
                query = text("""
                    SELECT
                        d.diary_id,
                        d.memo,
                        d.category_category_id,
                        d.mood_mood_id,
                        d.day_date,
                        u.name
                    FROM diary d
                    JOIN day ON day.date = d.day_date
                    JOIN users u ON u.user_id = day.users_user_id
                    WHERE day.date = :selected_date
                """)
                result = session.execute(query, {"selected_date": selected_date})
                rows = result.fetchall()

                if rows:
                    st.subheader(f"{selected_date}에 작성된 일기:")
                    for row in rows:
                        with st.container():
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.write(f"{row.name}")
                            with col2:
                                st.write(f"아이디: {row.diary_id}, 기분 포인트: {row.mood_mood_id}")
                                st.write(f"메모: {row.memo}")
                                st.write(f"작성일: {row.day_date.strftime('%Y-%m-%d')}")
                            st.divider()
                else:
                    st.warning("해당 날짜에 작성된 일기가 없습니다.")
            except Exception as e:
                st.error(f"일기를 가져오는 중 오류가 발생했습니다: {str(e)}")


def schedule_writing_page() :
   
    st.subheader("일정 작성")
    
    # 날짜 입력
    date = st.date_input(
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
                session.execute(insert_query, {"date": date, "user_id": 1})  # 예시로 user_id = 1로 설정
                
                # 커밋하여 변경 사항을 저장
                session.commit()
                
                # 성공 메시지
                st.success(f"{date} 날짜가 추가되었습니다.")
            except Exception as e:
                # 오류 발생 시 메시지 출력
                st.error(f"날짜 저장 중 오류가 발생했습니다: {str(e)}")

    # 시간 입력
    time = st.time_input("시간 입력")
    # 제목 입력
    title = st.text_input("일정 제목 입력")
    # 장소 입력
    location = st.text_input("장소 입력")
    # 메모 입력
    memo = st.text_area("메모 입력")

    if st.button("일정 저장"):
        with conn.session as session:
            try:
                # SQL 쿼리 실행 (날짜와 사용자 ID를 INSERT)
                insert_query = text("""
                    INSERT INTO schedule (title,location,memo,day_date, time)
                    VALUES (:title, :location,:memo,:day_date,time)
                """)
                
                # 실행할 데이터 준비
                session.execute(insert_query, {"title":title,"location":location,"memo":memo,"day_date": date, "time": time}) 
                # 커밋하여 변경 사항을 저장
                session.commit()
                # 성공 메시지
                st.success(f"{date} 날짜가 추가되었습니다.")
            except Exception as e:
                # 오류 발생 시 메시지 출력
                st.error(f"저장 중 오류가 발생했습니다: {str(e)}")

def show_schedule():
    query = """
        SELECT
           s.schedule_id,
           s.time,
           s.title,
           s.location,
           s.memo,
           s.day_date  
        FROM schedule s
    """
    df = conn.query(query, ttl=0)  # 데이터베이스에서 데이터를 조회합니다.

    for row in df.itertuples():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"{row.schedule_id}")
                st.write(f"{row.title}")
            with col2:
                st.write(f"장소: {row.location}")
                st.write(f"메모: {row.memo}") 
                st.write(f"날짜: {row.day_date }")
            st.divider()





def schedule_view_page():
    st.subheader("일정 확인 및 삭제")
    # 날짜 선택을 위한 입력 필드
    selected_date = st.date_input("일정을 확인할 날짜를 입력하세요:")

    # "날짜로 일정 확인" 버튼 클릭 시
    if st.button("날짜로 일정 확인"):
        with conn.session as session:
            try:
                # 선택된 날짜에 해당하는 일정만 조회하는 쿼리
                query = text("""
                    SELECT
                        s.schedule_id,
                        s.time,
                        s.title,
                        s.location,
                        s.memo,
                        s.day_date  
                    FROM schedule s
                    WHERE s.day_date = :selected_date
                """)
                result = session.execute(query, {"selected_date": selected_date})
                rows = result.fetchall()

                if rows:
                    st.subheader(f"{selected_date}에 작성된 일정:")
                    for row in rows:
                        with st.container():
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.write(f"{row.schedule_id}")
                                st.write(f"{row.title}")
                            with col2:
                                st.write(f"장소: {row.location}")
                                st.write(f"메모: {row.memo}") 
                                st.write(f"시간: {row.time}")
                                st.write(f"날짜: {row.day_date}")
                            st.divider()
                else:
                    st.warning(f"{selected_date}에 해당하는 일정이 없습니다.")
            except Exception as e:
                st.error(f"일정을 가져오는 중 오류가 발생했습니다: {str(e)}")

    # 기본적으로 모든 일정을 보여줍니다.
    st.subheader("모든 일정 확인")
    show_schedule()




# 페이지 선택
st.sidebar.title("페이지 선택")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["일기 작성", "일기 확인", "일정 작성", "일정 확인"]
)

if page == "일기 작성":
    diary_writing_page()
elif page == "일기 확인":
    view_page()
elif page == "일정 작성":
    schedule_writing_page()  # 일정 작성 함수
elif page == "일정 확인":
    schedule_view_page()     # 일정 확인 함수
