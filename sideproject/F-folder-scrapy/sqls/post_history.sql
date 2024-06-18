CREATE TABLE `post_history` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `post_id` int(1) unsigned comment 'ref, post.post_id',
  `ip` int(1) unsigned DEFAULT NULL,
  `port` smallint(1) unsigned DEFAULT NULL,
  `referrer` varchar(2048) DEFAULT NULL,
  `useragent` varchar(2048) NOT NULL,
  `created_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
