CREATE TABLE `assessment` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL,
  `member_id` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `status` varchar(32) NOT NULL COMMENT 'WAIT, REJECT, APPROVE',
  `reason` varchar(1024) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`pk`),
  UNIQUE KEY `assessment_indexer_1` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8