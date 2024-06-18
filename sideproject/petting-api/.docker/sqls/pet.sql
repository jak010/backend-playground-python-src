CREATE TABLE `pet` (
    `pk`              int(10) unsigned NOT NULL AUTO_INCREMENT,
    `nanoid`          char(24) NOT NULL,
    `owner`           char(24) NOT NULL,
    `name`            varchar(32) NOT NULL,
    `gender`          varchar(12) NOT NULL,
    `pdti`            varchar(32) DEFAULT NULL,
    `pdti_type`       varchar(4) DEFAULT NULL,
    `neutered_status` varchar(4) DEFAULT NULL,
    `breed`           varchar(128) DEFAULT NULL,
    `created_at`      datetime NOT NULL,
    `modified_at`     datetime NOT NULL,
    PRIMARY KEY (`pk`),
    UNIQUE KEY `pet_indexer_1` (`owner`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
