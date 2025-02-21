CREATE TABLE `member` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` int(1) unsigned DEFAULT NULL,
  `address1` VARCHAR(1024) DEFAULT NULL,
  `address2` VARCHAR(1024) DEFAULT NULL,

  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
