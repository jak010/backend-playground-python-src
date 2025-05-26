CREATE TABLE `member`
(
    `pk`       int(10) unsigned NOT NULL AUTO_INCREMENT,
    `nanoid`   char(24) NOT NULL,
    `name`     varchar(32)   DEFAULT NULL,
    `age`      tinyint(3) unsigned DEFAULT NULL,
    `address1` varchar(1024) DEFAULT NULL,
    `address2` varchar(1024) DEFAULT NULL,
    PRIMARY KEY (`pk`),
    KEY        `member_name_IDX` (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4



CREATE TABLE `member_profile`
(
    `pk`          int(1) unsigned NOT NULL AUTO_INCREMENT,
    `nanoid`      char(24) NOT NULL COMMENT 'ref, member.nanoid',
    `description` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO demo.member_profile (nanoid, description)
VALUES ('U3M065V1XtRa', '테스트 사용자 1'),
       ('U3M065V1XtRa', '테스트 사용자 2'),
       ('U3M065V1XtRa', '테스트 사용자 3'),
       ('U3M065V1XtRa', '테스트 사용자 4'),
       ('U3M065V1XtRa', '테스트 사용자 5'),
       ('u52ewaWbGLGt', '테스트 사용자 6'),
       ('u52ewaWbGLGt', '테스트 사용자 7'),
       ('u52ewaWbGLGt', '테스트 사용자 8'),
       ('u52ewaWbGLGt', '테스트 사용자 9'),
       ('u52ewaWbGLGt', '테스트 사용자 10');