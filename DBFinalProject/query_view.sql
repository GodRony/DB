-- 1번 --
SELECT p.post_id, u.name
FROM posts p
JOIN users u ON p.author_id = u.user_id
WHERE p.price > (SELECT AVG(price) FROM posts);

-- 2번 --
DROP VIEW IF EXISTS user_post_count;

CREATE VIEW user_post_count AS
SELECT p.author_id, COUNT(p.post_id) AS post_count
FROM posts p
GROUP BY p.author_id;

SELECT u.name, u.user_id
FROM user_post_count upc
JOIN users u ON upc.author_id = u.user_id
WHERE upc.post_count >= 2;


-- 3번 --
DROP VIEW IF EXISTS completed_transactions;

CREATE VIEW completed_transactions AS
SELECT u.name AS buyer_name, fp.final_price, t.status
FROM transactions t
JOIN users u ON t.buyer_id = u.user_id
JOIN finalprices fp ON t.finalPrice_id = fp.final_price_id
WHERE t.status = '거래완료';

SELECT buyer_name, final_price
FROM completed_transactions
WHERE status = '거래완료';


 SELECT * FROM completed_transactions;

-- 4번 --
SELECT buyer_name, SUM(final_price) AS total_spent
FROM completed_transactions
GROUP BY buyer_name
ORDER BY total_spent DESC
LIMIT 1;
