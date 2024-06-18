CREATE TABLE `session` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `session_id` char(36) NOT NULL,
  `member_id` char(36) NOT NULL,
  `iat` int(1) unsigned NOT NULL,
  `exp` int(1) unsigned NOT NULL,
  `created_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;