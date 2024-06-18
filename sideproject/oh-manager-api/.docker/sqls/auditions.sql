CREATE TABLE `auditions` (
  `id` bigint(1) unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(32) NOT NULL COMMENT '플랫폼에서 구분되는 게시번호',
  `platform` varchar(32) NOT NULL COMMENT '수집 플랫폼',
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `category` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `reward` varchar(255) DEFAULT NULL,
  `link` varchar(1028) DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `created_at` int(1) unsigned NOT NULL,
  `modified_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;