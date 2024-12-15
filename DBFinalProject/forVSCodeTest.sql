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