CREATE TABLE `member_asset` (
  `pk` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `type` varchar(12) NOT NULL,
  `issued_quantity` int(1) unsigned DEFAULT '0',
  `reason` varchar(1024) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;