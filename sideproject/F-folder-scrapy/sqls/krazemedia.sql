CREATE TABLE `krazemedia` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `trace_id` char(36) NOT NULL,
  `is_convert` tinyint(1) unsigned DEFAULT '0',
  `reference_id` BIGINT unsigned DEFAULT NULL,
  `reference_date` datetime NOT NULL,
  `reference_link` varchar(5012) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` text NOT NULL,
  `thumbnail` TEXT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `krazemedia_index` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
