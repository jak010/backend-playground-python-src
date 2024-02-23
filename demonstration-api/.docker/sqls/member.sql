CREATE TABLE `member` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` char(24) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` int(1) unsigned DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
