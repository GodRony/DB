-- REGIONS --
CREATE TABLE regions (
    region_id INT NOT NULL PRIMARY KEY, 
    region_name VARCHAR(45)            
);

-- USER  --
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
CREATE TABLE posts (
    post_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(45),
    title VARCHAR(45),
    price FLOAT,
    created_date DATE,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

-- CHATROOMS ---
CREATE TABLE chatrooms (
    chatroom_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    posts_post_id INT NOT NULL,
    FOREIGN KEY (posts_post_id) REFERENCES posts(post_id)
);

-- CHATS --
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
CREATE TABLE finalprices (
    final_price_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    posts_post_id INT NOT NULL,
    final_price FLOAT,
    FOREIGN KEY (posts_post_id) REFERENCES posts(post_id)
);

ALTER TABLE finalprices
ADD CONSTRAINT fk_posts_post_id
FOREIGN KEY (posts_post_id) REFERENCES posts(post_id);

-- TRANSACTIONS --
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
