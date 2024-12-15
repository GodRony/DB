-- REGIONS --
INSERT INTO regions (region_name)
VALUES ('춘천시 퇴계동'),
       ('춘천시 소양동'),
       ('춘천시 우두동');
       
select * from regions;

-- USER  --
DELETE FROM users;
select * from users;
SET SQL_SAFE_UPDATES = 0;
INSERT INTO users (user_id,regions_region_id, name, alias, email, address, join_date)
VALUES
    (1,(SELECT region_id FROM regions WHERE region_name = '춘천시 퇴계동'), '김철수', 'cheol777', 'cs.kim@hallym.ac.kr', '강원도 춘천시 퇴계동 A 아파트', '2021-01-10'),
    (2,(SELECT region_id FROM regions WHERE region_name = '춘천시 소양동'), '이영희', 'lyh004', 'yh.lee@hallym.ac.kr', '강원도 춘천시 소양동 B빌라', '2023-02-15'),
    (3,(SELECT region_id FROM regions WHERE region_name = '춘천시 우두동'), '박민수', 'soosoo', 'ms.park@hallym.ac.kr', '강원도 춘천시 우두동 C원룸', '2022-03-20'),
    (4,(SELECT region_id FROM regions WHERE region_name = '춘천시 퇴계동'), '최수정', 'crystal_choi', 'sj.choi@hallym.ac.kr', '강원도 춘천시 퇴계동 D아파트', '2024-04-25'),
    (5,(SELECT region_id FROM regions WHERE region_name = '춘천시 우두동'), '홍길동', 'west_south8', 'gd.hong@hallym.ac.kr', '강원도 춘천시 우두동 E빌리지', '2023-05-30');

-- POST --
describe posts;
select * from posts;
DELETE FROM posts;
DROP TABLE IF EXISTS posts;
TRUNCATE TABLE posts;
ALTER TABLE posts AUTO_INCREMENT = 1;  -- AUTO_INCREMENT 값을 초기화하는 방법: (GPT야 사랑해) --


INSERT INTO posts (category, title, price, created_date, author_id)
VALUES
    ('전자제품', '김치냉장고 다시 팝니다', 90000, '2024-11-29', (SELECT user_id FROM users WHERE name = '김철수')),
    ('전자제품', '김치냉장고 다시 팝니다', 90000, '2024-11-29', (SELECT user_id FROM users WHERE name = '김철수')),
    ('의류', '유광 패딩 사이즈 100', 5000, '2024-12-01', (SELECT user_id FROM users WHERE name = '이영희')),
    ('가구', '수납장', 80000, '2024-12-01', (SELECT user_id FROM users WHERE name = '박민수')),
    ('도서', '디즈니 영어책 총8권', 10000, '2024-12-02', (SELECT user_id FROM users WHERE name = '최수정')),
    ('전자제품', '상태좋은 전자레인지', 50000, '2024-12-03', (SELECT user_id FROM users WHERE name = '홍길동')),
    ('전자제품', '건조기 팝니다 (이사)', 90000, '2024-12-03', (SELECT user_id FROM users WHERE name = '박민수')),
    ('뷰티', '필링젤', 12000, '2024-12-03', (SELECT user_id FROM users WHERE name = '홍길동')),
    ('의류', '나이키 기모맨투맨', 40000, '2024-12-04', (SELECT user_id FROM users WHERE name = '김철수'));



-- CHATROOMS ---
describe chatrooms;
DELETE FROM chatrooms;
select * from chatrooms; 
DROP TABLE IF EXISTS chatrooms;

CREATE TABLE chatrooms (
    chatroom_id INT NOT NULL PRIMARY KEY,  -- 기본 키로 chatroom_id 설정
    posts_post_id INT NOT NULL           -- 단일 외래 키로 posts_post_id 설정
   
);
ALTER TABLE chatrooms
    MODIFY chatroom_id INT NOT NULL AUTO_INCREMENT;
           -- chatroom_id만 기본 키로 설정

INSERT INTO chatrooms (chatroom_id, posts_post_id)
VALUES
    (1, 1),  -- 첫 번째 채팅방, 첫 번째 게시글에 대한 채팅방
    (2, 2),  -- 두 번째 채팅방, 두 번째 게시글에 대한 채팅방
    (3, 3);  -- 세 번째 채팅방, 세 번째 게시글에 대한 채팅방
INSERT INTO chatrooms (chatroom_id, posts_post_id)
VALUES
    (4, 4), 
    (5, 5), 
    (6, 6),  
	(7, 7),
	(8, 8),
	(9, 9);




SELECT * FROM posts;

-- CHATS --
describe chats;
select * from chats;
DELETE FROM chats;
DROP TABLE IF EXISTS chats;
TRUNCATE TABLE chats;

CREATE TABLE chats (
    chatroom_id INT NOT NULL,
    interested_user_id INT NOT NULL,
    content TEXT,
    manner_rating INT,
    last_update_date DATETIME,
    PRIMARY KEY (chatroom_id, interested_user_id), -- 복합 기본 키 설정 (post_id 제외)
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms(chatroom_id), -- chatrooms 테이블의 chatroom_id 참조
    FOREIGN KEY (interested_user_id) REFERENCES users(user_id) -- users 테이블의 user_id 참조
);

INSERT INTO chats (chatroom_id, interested_user_id, content, manner_rating, last_update_date)
VALUES
    (1, (SELECT user_id FROM users WHERE name = '이영희'), '대면 거래 가능한가요?', NULL, '2024-11-30'),
    (1, (SELECT user_id FROM users WHERE name = '최수정'), '좋은 가격에 잘 샀습니다.', 5, '2024-12-05'),
    (3, (SELECT user_id FROM users WHERE name = '홍길동'), '빠른 거래 감사합니다', 5, '2024-12-05'),
    (5, (SELECT user_id FROM users WHERE name = '박민수'), '네고 원합니다', NULL, '2024-12-04'),
    (6, (SELECT user_id FROM users WHERE name = '홍길동'), '매우 만족합니다', 5, '2024-12-05');



-- FINALPRICES --
describe finalprices;
select * from finalprices;
DELETE FROM finalprices;
DROP TABLE IF EXISTS finalprices;
TRUNCATE TABLE finalprices;
ALTER TABLE finalprices AUTO_INCREMENT = 1; 

-- 1. finalprices 테이블에 final_price_id 추가
ALTER TABLE finalprices
ADD final_price_id INT AUTO_INCREMENT PRIMARY KEY;

-- 2. 기존 posts_post_id에서 PRIMARY KEY 제거
ALTER TABLE finalprices
DROP PRIMARY KEY;

-- 3. posts_post_id를 FOREIGN KEY로 설정 (posts 테이블의 post_id를 참조)
ALTER TABLE finalprices
ADD CONSTRAINT fk_posts_post_id
FOREIGN KEY (posts_post_id) REFERENCES posts(post_id);



INSERT INTO finalprices (posts_post_id, final_price) 
VALUES
    (1, 90000),
    (4, 80000),
	(5, 10000),
    (6, 50000),
    (7, 90000);



-- TRANSACTIONS --
describe transactions;
select * from transactions;
DELETE FROM transactions;
DROP TABLE IF EXISTS transactions;
TRUNCATE TABLE transactions;

INSERT INTO transactions(transaction_id,posts_post_id,finalPrice_id,buyer_id,status,last_update_date)
VALUES
	(1,1,1,(SELECT user_id FROM users WHERE name = '최수정'),'거래완료','2024-12-4'),
	(2,4,2,(SELECT user_id FROM users WHERE name = '홍길동'),'거래완료','2024-12-4'),
	(3,5,3,(SELECT user_id FROM users WHERE name = '김철수'),'예약중','2024-12-4'),
	(4,6,4,(SELECT user_id FROM users WHERE name = '박민수'),'예약중','2024-12-5'),
	(4,7,5,(SELECT user_id FROM users WHERE name = '홍길동'),'거래완료','2024-12-5');
    
    





