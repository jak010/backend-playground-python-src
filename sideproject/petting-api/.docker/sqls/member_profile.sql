CREATE TABLE `member_profile` (
    `pk`           int(1) unsigned NOT NULL AUTO_INCREMENT,
    `nanoid`       char(24) NOT NULL COMMENT 'ref, member.nanoid',
    `nickname`     varchar(64) NOT NULL,
    `description`  varchar(300) DEFAULT NULL,
    `address`      varchar(1024) DEFAULT NULL,
    `region1`      varchar(128) DEFAULT NULL,
    `region2`      varchar(128) DEFAULT NULL,
    `region3`      varchar(128) DEFAULT NULL,
    `road_name`    varchar(128) DEFAULT NULL,
    `latitude`     double(10,6) DEFAULT NULL COMMENT 'ìœ„ë„',
    `longitude`    double(10,6) DEFAULT NULL COMMENT 'ê²½ë„',
    `job`          varchar(24) DEFAULT NULL,
    `birthday`     datetime NOT NULL,
    `gender`       varchar(16) NOT NULL,
    `mbti`         char(4) DEFAULT NULL,
    `created_at`   datetime NOT NULL,
    `modified_at`  datetime NOT NULL,
    PRIMARY KEY (`pk`),
    UNIQUE KEY `member_profile_index` (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;