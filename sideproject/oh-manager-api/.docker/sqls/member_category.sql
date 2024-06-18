CREATE TABLE `member_category` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` char(36) NOT NULL,
  `primary` varchar(12) NOT NULL,
  `secondary` varchar(12) NOT NULL,
  `created_at` int(1) unsigned NOT NULL,
  `modified_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `member_category` (`member_id`,`primary`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;