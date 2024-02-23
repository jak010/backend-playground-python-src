CREATE TABLE `member_profile` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` char(24) NOT NULL COMMENT 'ref, member.memberid',
  `description` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
