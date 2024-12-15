-- REGIONS --
describe regions;
CREATE TABLE regions (
    region_id INT NOT NULL PRIMARY KEY, 
    region_name VARCHAR(45)            
);
-- USER  --
describe users;
DELETE FROM users;
select * from users;
SET SQL_SAFE_UPDATES = 0;

CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    regions_region_id INT NOT NULL,
    name VARCHAR(45),
    alias VARCHAR(45),
    email VARCHAR(45),
    address VARCHAR(45),
    join_date DATE,
    FOREIGN KEY (regions_region_id) REFERENCES regions(region_id)
);

-- POST --
describe posts;
select * from posts;
DELETE FROM posts;
DROP TABLE IF EXISTS posts;
TRUNCATE TABLE posts;
ALTER TABLE posts AUTO_INCREMENT = 1;  -- AUTO_INCREMENT 값을 초기화하는 방법: (GPT야 사랑해) --

CREATE TABLE posts (
    post_id INT NOT NULL PRIMARY KEY,
    category VARCHAR(45),
    title VARCHAR(45),
    price FLOAT,
    created_date DATE,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);


-- CHATROOMS ---
describe chatrooms;
DELETE FROM chatrooms;
select * from chatrooms; 
DROP TABLE IF EXISTS chatrooms;

CREATE TABLE chatrooms (
    chatroom_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    posts_post_id INT NOT NULL,
    FOREIGN KEY (posts_post_id) REFERENCES posts(post_id)
);

ALTER TABLE chatrooms
    MODIFY chatroom_id INT NOT NULL AUTO_INCREMENT;
           -- chatroom_id만 기본 키로 설정
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



-- FINALPRICES --
describe finalprices;
select * from finalprices;
DELETE FROM finalprices;
DROP TABLE IF EXISTS finalprices;
TRUNCATE TABLE finalprices;
ALTER TABLE finalprices AUTO_INCREMENT = 1; 

CREATE TABLE finalprices (
    final_price_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    posts_post_id INT NOT NULL,
    final_price FLOAT,
    FOREIGN KEY (posts_post_id) REFERENCES posts(post_id)
);


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


-- TRANSACTIONS --
describe transactions;
select * from transactions;
DELETE FROM transactions;
DROP TABLE IF EXISTS transactions;
TRUNCATE TABLE transactions;

CREATE TABLE transactions (
    transaction_id INT NOT NULL,
    posts_post_id INT NOT NULL,
    finalPrice_id INT,
    buyer_id INT,
    status VARCHAR(45),
    last_update_date DATE,
    PRIMARY KEY (transaction_id, posts_post_id),
    FOREIGN KEY (posts_post_id) REFERENCES posts(post_id),
    FOREIGN KEY (finalPrice_id) REFERENCES finalprices(final_price_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id)
);





