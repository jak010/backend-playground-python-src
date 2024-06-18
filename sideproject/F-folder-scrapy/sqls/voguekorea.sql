CREATE TABLE `voguekorea` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `trace_id` char(36) NOT NULL,
  `is_convert` tinyint(1) unsigned DEFAULT '0',
  `reference_id` int(1) unsigned NOT NULL,
  `reference_date` datetime NOT NULL,
  `reference_link` varchar(5012) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` mediumtext NOT NULL,
  `thumbnail` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vougekorea_index` (`reference_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;