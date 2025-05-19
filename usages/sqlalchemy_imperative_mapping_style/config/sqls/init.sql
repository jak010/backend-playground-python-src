CREATE TABLE `member` (
  `pk` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nanoid` CHAR(24) NOT NULL,
  `name` VARCHAR(32) DEFAULT NULL,
  `age` TINYINT UNSIGNED DEFAULT NULL,
  `address1` VARCHAR(1024) DEFAULT NULL,
  `address2` VARCHAR(1024) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `member_profile` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `description` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
