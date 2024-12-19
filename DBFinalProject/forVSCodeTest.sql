-- 나머지 --
SELECT
     p.title,
     p.price,
     u.alias,
     r.region_name
FROM posts p
JOIN users u ON u.user_id = p.author_id
JOIN regions r ON r.region_id =u.regions_region_id
JOIN transactions t ON t.posts_post_id = p.post_id;

SELECT
     p.title,
     p.price,
     u.alias
FROM posts p
JOIN users u ON u.user_id = p.author_id;

SELECT
     p.title,
     p.price,
     r.region_name
FROM posts p
JOIN users u ON u.user_id = p.author_id
JOIN regions r ON r.region_id = u.regions_region_id;


SELECT * FROM  users;
SELECT * FROM  posts;
SELECT * FROM  regions;

SELECT
     p.title,
     p.price,
     u.alias,
     r.region_name
FROM posts p
JOIN users u ON u.user_id = p.author_id
JOIN regions r ON r.region_id =u.regions_region_id
JOIN transactions t ON t.posts_post_id = p.post_id
WHERE r.region_name = "춘천시 퇴계동";

SELECT
     p.title,
     p.price,
     u.alias,
     r.region_name
FROM posts p
JOIN users u ON u.user_id = p.author_id
JOIN regions r ON r.region_id =u.regions_region_id
JOIN transactions t ON t.posts_post_id = p.post_id;

SELECT * FROM users;
describe posts;


SELECT * FROM transactions;

INSERT INTO posts (category, title, price, created_date, author_id)
values ('전자제품', '테스트전자제품', 10000, '2024-12-20',18);

SELECT * FROM posts;

SELECT alias, user_id FROM users WHERE alias = 'cheol777';

SELECT regions_region_id, name FROM users; 
SELECT * FROM regions;

SELECT r.region_name name , u.name
FROM users u
JOIN regions r ON u.regions_region_id = r.region_id
WHERE u.user_id = 18;

SELECT * FROM posts;
SELECT * FROM transactions;

SELECT * FROM chatrooms;

INSERT INTO transactions (posts_post_id,finalPrice_id,buyer_id,status,last_update_date)
VALUES();

describe chatrooms;
INSERT INTO chatrooms (posts_post_id)
VALUES();

SELECT * FROM chats;


SELECT
*
        FROM posts p
        JOIN users u ON u.user_id = p.author_id
        JOIN regions r ON r.region_id =u.regions_region_id
        JOIN transactions t ON t.posts_post_id = p.post_id
        JOIN chatrooms c ON c.posts_post_id = p.post_id;
SELECT * FROM chatrooms;

SELECT chatroom_id FROM chatrooms WHERE posts_post_id =19;

 SELECT chatroom_id FROM chatrooms WHERE posts_post_id = 19;
 

 
 SELECT u.alias, c.content, c.manner_rating, c.last_update_date
 FROM chats c
 JOIN users u ON u.user_id = c.interested_user_id
 WHERE c.chatroom_id = 5;
 
SELECT * FROM chats ; 

SELECT
*
FROM posts p
JOIN users u ON u.user_id = p.author_id
JOIN regions r ON r.region_id =u.regions_region_id
JOIN transactions t ON t.posts_post_id = p.post_id;
        
SELECT * FROM transactions;
