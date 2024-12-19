-- 1번 문제 --
UPDATE chats
SET content = '네고 감사합니다'
WHERE chatroom_id = 4;

select * from chats;

-- 2번 문제 --
-- finalprices 테이블에서 final_price를 5000원 차감
UPDATE finalprices
SET final_price = final_price - 5000
WHERE final_price_id = (
    SELECT finalPrice_id 
    FROM transactions 
    WHERE transaction_id = 4
);

SELECT * FROM final_price_id;


-- transactions 테이블에서 status를 '거래완료'로 변경하고, last_update_date를 현재 날짜로 설정
-- 3번 문제 --
DELETE FROM transactions
WHERE posts_post_id = 2;



-- test ---
UPDATE transactions
SET status = '거래완료', last_update_date = CURDATE()
WHERE transaction_id = 4;

select * from transactions;
select * from finalprices;

select finalPrice_id from transactions where transaction_id = 4;

UPDATE transactions
SET transaction_id = 5
WHERE posts_post_id = 6;

UPDATE transactions
SET finalPrice_id = 7
WHERE transaction_id = 2;
