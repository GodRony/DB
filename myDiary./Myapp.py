import streamlit as st


st.set_page_config(
     page_title = 'MyDiary',
     page_icon= ':shark:',
     layout='wide',
     initial_sidebar_state='auto'
)

# # 타이틀
st.title('일기 및 일정관리 앱')

# #헤더
# st.header('일기작성')

# #세션 스테이트 초기화

# if 'category' not in st.session_state:
#     st.session_state['category'] = ''

# if 'feeling' not in st.session_state:
#     st.session_state['feeling'] = ''
    
# if 'memo' not in st.session_state:
#     st.session_state['memo'] = ''
    
# DB 연결
conn = st.connection('sqlite_db', type='sql')


# def diary_writing_page():
#     st.title()
    
#     st.subheader("일기작성")
    
#     category = st.selectbox("카테고리",["일상","여행","운동"])
#     mood = st.selectbox("기분",["매우 나쁨","나쁨","보통","좋음","매우좋음"])
#     st.write("포인트:",1)
#     memo = st.text_area("메모")
#     photo = st.file_uploader("사진 업로드",type=["png","jpg","jpeg"])
    
#     if st.button("일기 저장"):
#         with conn.session as session:
#             try:
#                 category_id = conn.query(f"SELECT category_id FROM
#                                          categories WHERE category_name = 
#                                          '{category}'").iloc[0]['category_id']
#                 mood_name = ''.join(mood.split()[:-1])
#                 mood_id = conn.query(f"SELECT mood_id FROM moods 
#                                      WHERE mood_name = '{mood_name}'").iloc[0]['mood_id']
#                 session.execute(text("""
#                     INSERT INTO diaries (user_id, category_id, mood_id,memo)
#                     VALUES (:user_id, : category_id, :mood_id, :memo)
#                 """),{
#                     "user_id":1,
#                     "category_id":category_id,
#                 })
                
#                 st.success("일기가 저장되었습니다!")
                
#             except Exception as e:
#                 st.error(f"저장 중 오류가 발생했습니다: {str(e)}")

# def show_diaries():
#     query = """
#         SELECT
#             d.diary_id,
#             u.name as user_name,
#             u.profile_image,
#             m.mood_name as mood,
#             d.memo,
#             d.created_at
#         FROM diaries d
#         JOIN users u ON d.user_id = u.user_id
#         JOIN moods m ON d.mood_id = m.mood_id
#         ORDER BY d.created_at DESC;
#     """
    
#     df = conn.query(query,ttl=0)
    
#     delete_diary_id = None
    
#     for row in df.itertuples():
#         with st.container():
#             col1, col2 = st.columns([1,4])
#             with col1:
#                 st.write(f"{row.user_name} :{row.profile_image}:")
#             with col2:
#                 st.write(f"{row.diary_id}*{row.mood}")
#                 st.write(row.memo)
#                 st.write(f"작성일: {row.created_at.strftime('%Y-%m-%d %H:%M')}")
#             st.divider()


# def view_page():
#     st.title("일기 보기")
#     st.subheader("일기 삭제")
#     diary_id_to_delete = st.text_input("삭제할 일기의 ID를 입력하세요:")           

#     if st.button("일기 삭제",type = 'primary'):
#         if diary_id_to_delete.strip():
#             try:
#                 diary_id = int(diary_id_to_delete)
#                 with conn.session as session:
#                     delete_query = text("DELETE FROM diaries WHERE diary_id = :diary_id")
#                     result = session.execute(delete_query,{"diary_id":diary_id})
#                     session.commit()
                    
#                     if result.rowcount > 0:
#                         st.success("일기가 삭제되었습니다!")
#                         st.rerun()
#                     else:
#                         st.warning("해당 ID의 일기를 찾을 수 없습니다.")
#             except ValueError :
#                 st.error("올바른 숫자 형식의 ID를 입력해주세요.")
#             except Exception as e :
#                 st.error(f"삭제 중 오류가 발생했습니다: {str(e)}")
#     show_diaries()
    
st.slider.title("페이지 선택")
page = st.slider.radio("이동할 페이지를 선택하세요",["일기 작성","일기 확인"])


#if page == "일기 작성":
    
    # diary_writing_page()
#elif page == "일기 확인":
    # view_page()