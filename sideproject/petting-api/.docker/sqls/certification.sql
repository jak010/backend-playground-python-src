CREATE TABLE `certification` (
    `pk`         INT(1) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `nanoid`     CHAR(24) NOT NULL,
    `member_id`  CHAR(24) NOT NULL COMMENT 'ref, member.nanoid',
    `phone`      varchar(20) DEFAULT NULL,
    `type`       VARCHAR(12) NOT NULL COMMENT '인증 타입',
    `code`       VARCHAR(12) NOT NULL COMMENT '인증 코드',
    `status`     VARCHAR(12) NOT NULL COMMENT '진행 상태',
    `created_at` DATETIME NOT NULL,
    `modified_at` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
