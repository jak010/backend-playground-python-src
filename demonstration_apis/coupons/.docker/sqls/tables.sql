CREATE TABLE `coupons` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL COMMENT '쿠폰 제목',
    `coupon_type` VARCHAR(255) NOT NULL COMMENT '쿠폰 종류',
    `total_quantity` INT NOT NULL COMMENT '발급 총 수량',
    `issued_quantity` INT NULL COMMENT '쿠폰 발급 최대 수량',
    `discount_amount` INT NOT NULL COMMENT '할인 금액',
    `min_available_amount` INT NOT NULL COMMENT '최소 사용 금액',
    `date_issue_start` DATETIME(6) NOT NULL COMMENT '쿠폰 발급 시작일',
    `date_issue_end` DATETIME(6) NOT NULL COMMENT '쿠폰 발급 종료일',
    `date_created` DATETIME(6) NOT NULL,
    `date_updated` DATETIME(6) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '쿠폰 정책';

-- Coupon Issues Table
CREATE TABLE `coupon_issues` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `coupon_id` BIGINT(20) NOT NULL COMMENT '쿠폰 ID',
    `user_id` BIGINT(20) NOT NULL COMMENT '사용자 ID',
    `date_issued` DATETIME(6) NOT NULL COMMENT '발급 일자',
    `date_used` DATETIME(6) NULL COMMENT '사용 일자',
    `date_created` DATETIME(6) NOT NULL,
    `date_updated` DATETIME(6) NOT NULL COMMENT '업데이트 일자',
    PRIMARY KEY (`id`),
    UNIQUE KEY `coupon_issue_index` (`coupon_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '쿠폰 발급 내역';

CREATE DATABASE IF NOT EXISTS test_coupons;

-- 날짜는 조정
INSERT INTO coupons.coupons (id, title, coupon_type, total_quantity, issued_quantity, discount_amount, min_available_amount, date_issue_start, date_issue_end, date_created, date_updated)
VALUES(1, '네고왕 선착순 쿠폰', '1', 100, 0, 100000, 110000, '2024-02-01 00:00:00', '2024-02-10 00:00:00', '2024-02-03 00:00:00', '2024-02-03 00:00:00');
