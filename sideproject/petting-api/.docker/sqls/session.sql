CREATE TABLE `session` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL,
  `member_id` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `channel` varchar(24) DEFAULT NULL,
  `channel_code` varchar(1024) DEFAULT NULL,
  `issued_time` int(10) unsigned NOT NULL,
  `expire_time` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;