CREATE TABLE `member_profile` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `member_nanoid` char(24) NOT NULL,
  `description` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;