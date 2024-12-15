import streamlit as st
from sqlalchemy.sql import text

# DB 연결
conn = st.connection('mysql', type='sql')

df = conn.query('SELECT * FROM posts LIMIT 5;', ttl=600)

import streamlit as st
import pandas as pd

# DB 연결 (여기서는 예시로 연결을 가정)
# conn = ...

def get_posts():
    # SQL 쿼리
    query = """
        SELECT
            p.title,
            p.price,
            u.alias,
            r.region_name
        FROM posts p
        JOIN users u ON u.user_id = p.author_id
        JOIN regions r ON r.region_id =u.regions_region_id
        JOIN transactions t ON t.posts_post_id = p.post_id;
    """
    
    # 쿼리 실행 후 pandas DataFrame으로 변환
    df = conn.query(query, ttl=0)

    # 게시물 UI 표시
    for row in df.itertuples():  # DataFrame에서 itertuples()를 사용하여 반복
        with st.container():
            col1, col2 = st.columns([1, 4])  # 두 개의 컬럼을 사용해서 레이아웃을 나눔
            with col1:
                # 사용자 별칭(alias) 출력
                st.write(f"**{row.alias}**")  # 별칭을 굵게 표시
            with col2:
                # 제목, 가격, 지역명 출력
                st.write(f"**제목**: {row.title}")
                st.write(f"**가격**: {row.price} 원")
                st.write(f"**지역**: {row.region_name}")

            # 항목 사이에 구분선
            st.divider()

def get_posts_selected_city(city) :
    # SQL 쿼리 (파라미터 바인딩을 사용하여 지역을 안전하게 전달)
      with conn.session as session:
            try:
                query = text("""
                    SELECT
                        p.title,
                        p.price,     
                        u.alias,    
                        r.region_name
                    FROM posts p
                    JOIN users u ON u.user_id = p.author_id
                    JOIN regions r ON r.region_id =u.regions_region_id
                    JOIN transactions t ON t.posts_post_id = p.post_id
                    WHERE r.region_name = :city
                """)
                result = session.execute(query, {"city": city})
                rows = result.fetchall()

                # 게시물 UI 표시
                if rows : 
                    for row in rows:  
                        with st.container():
                            col1, col2 = st.columns([1, 4])  # 두 개의 컬럼을 사용해서 레이아웃을 나눔
                            with col1:
                                st.write(f"**{row.alias}**")  # 별칭을 굵게 표시
                            with col2:
                                st.write(f"**제목**: {row.title}")
                                st.write(f"**가격**: {row.price} 원")
                                st.write(f"**지역**: {row.region_name}")
                            st.divider()
                else:
                    st.warning("해당 날짜에 작성된 일기가 없습니다.")
            except Exception as e:
                st.error(f"일기를 가져오는 중 오류가 발생했습니다: {str(e)}")


def view_page():
    
    st.subheader("게시글 조회")
    city = st.selectbox("동네 선택:", ["춘천시 퇴계동", "춘천시 소양동", "춘천시 우두동", "전체"])

    # city가 '전체'로 선택되지 않은 경우 선택된 동네에 맞는 게시물 조회
    if city != "전체":
        get_posts_selected_city(city)
    else:
        get_posts()  # city가 선택되지 않았으면 전체 게시물 조회



def get_city_id(city_name):
    try:
        # SQL 쿼리 준비
        query = f"""
        SELECT region_id 
        FROM regions 
        WHERE region_name = '{city_name}'
        """
        
        # 쿼리 실행 (하나의 값만 반환)
        result = conn.query(query).iloc[0]  # 결과에서 첫 번째 행을 가져옴
        region_id = result['region_id']
        
        # region_id 반환
        st.success("region_id를 찾았습니다!")
        return region_id

    except Exception as e:
        # 오류 발생 시 에러 메시지 표시
        st.error(f"region_id를 찾는데 오류가 발생했어요: {str(e)}")
        return None   

# 초기 로그인 상태 설정 (세션 상태로 관리)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # 초기 로그인 상태는 False
if 'user' not in st.session_state:
    st.session_state.user = ""  # 초기 user 정보는 빈 문자열

# 로그인 상태에 따라 알림 메시지를 표시하는 함수
def display_login_status():
    if not st.session_state.logged_in:
        st.sidebar.error("로그인이 필요합니다.")
    else:
        st.sidebar.success(f"{st.session_state.user}님으로 로그인이 되었습니다!")

# 페이지 타이틀 설정
st.sidebar.title("한림마켓")

# 로그인 상태에 따라 메시지 표시
display_login_status()

# 페이지 선택
page = st.sidebar.radio("원하는 작업을 선택하세요:", ("로그인", "회원가입"))

# 로그인 페이지
if page == "로그인":
    st.sidebar.subheader("로그인")
    
    # 사용자 선택 (예시로 간단히 사용자 이름을 선택하는 방식)
    user = st.sidebar.selectbox("사용자를 선택하세요:", ["사용자1", "사용자2", "사용자3"])
    
    # 로그인 버튼
    if st.sidebar.button("로그인"):
        # 로그인 버튼을 클릭하면 세션 상태의 logged_in을 True로 변경하고, 선택한 사용자 정보를 저장
        st.session_state.logged_in = True
        st.session_state.user = user  # 선택한 사용자 이름을 세션 상태에 저장
        st.sidebar.success(f"{user}님으로 로그인이 되었습니다!")
        st.write(f"{user}님, 로그인 성공!")

# 회원가입 페이지
elif page == "회원가입":
    st.sidebar.subheader("회원가입")
    
    # 회원가입 폼
    name = st.sidebar.text_input("이름")
    alias = st.sidebar.text_input("별칭")
    email = st.sidebar.text_input("이메일")
    address = st.sidebar.text_input("주소")
    join_date = st.sidebar.text_input("가입일")
    city = st.sidebar.selectbox("동네 선택:", ["춘천시 퇴계동", "춘천시 소양동", "춘천시 우두동"])
    
# 가입하기 버튼
if st.sidebar.button("가입하기"):
    if name and alias and email and address:  # 모든 항목을 체크
        with conn.session as session:
            try:
                region_id = get_city_id(city)  # 지역 ID 가져오기

                # SQL 쿼리 준비
                insert_query = text("""
                    INSERT INTO users (regions_region_id, name, alias, email, address, join_date)
                    VALUES (:regions_region_id, :name, :alias, :email, :address, :join_date)
                """)

                # 실행할 데이터 준비
                session.execute(insert_query, {
                    "regions_region_id": region_id,
                    "name": name,
                    "alias": alias,
                    "email": email,
                    "address": address,
                    "join_date": join_date
                })

                # 커밋하여 변경 사항을 저장
                session.commit()

                # 성공 메시지
                st.sidebar.success(f"{name}님, 회원가입이 완료되었습니다!")

            except Exception as e:
                # 예외 처리
                st.error(f"DB 저장 중 오류가 발생했습니다: {str(e)}")

    else:
        # 필수 항목이 빈 값일 경우
        st.error("모든 항목을 입력해주세요.")


view_page()
