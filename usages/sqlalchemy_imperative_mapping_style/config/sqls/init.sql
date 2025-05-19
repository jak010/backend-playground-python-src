CREATE TABLE `member` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` tinyint(3) unsigned DEFAULT NULL,
  `address1` varchar(1024) DEFAULT NULL,
  `address2` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `member_name_IDX` (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4



CREATE TABLE `member_profile` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `description` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
