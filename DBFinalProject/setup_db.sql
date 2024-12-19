-- 데이터베이스 및 계정 셋팅 스크립트
-- 학번 예제: 20213236

-- 1. 데이터베이스 생성
CREATE DATABASE finals_20213236_CASE01;

-- 2. 계정 생성 및 비밀번호 설정
CREATE USER 'final_exam_20213236'@'localhost' IDENTIFIED BY 'case01';

-- 3. 새로 생성한 계정에 데이터베이스에 대한 권한 부여
GRANT ALL PRIVILEGES ON finals_20215177_CASE01.* TO 'final_exam_20213236'@'localhost';

-- 4. 변경 사항 적용
FLUSH PRIVILEGES;
