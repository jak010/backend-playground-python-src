CREATE TABLE `member` (
  `id` char(36) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` char(60) NOT NULL,
  `is_active` tinyint(1) unsigned DEFAULT NULL COMMENT '0:비활성화, 1:활성화',
  `joined_at` int(1) NOT NULL,
  `created_at` int(1) NOT NULL,
  `modified_at` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `member_index` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;