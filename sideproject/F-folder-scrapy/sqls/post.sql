CREATE TABLE `post` (
  `post_id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `trace_id` char(36) NOT NULL,
  `views` int(1) unsigned NOT NULL DEFAULT '0',
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '0:미삭제, 1:삭제',
  `is_temporary` tinyint(1) DEFAULT '0',
  `title` varchar(5012) NOT NULL,
  `content` text COMMENT 'llm으로 변환된 콘텐츠',
  `keyword` text COMMENT 'llm으로 변환된 키워드',
  `platform` varchar(36) NOT NULL,
  `reference_link` varchar(5012) NOT NULL,
  `thumbnail` varchar(1024) NOT NULL,
  `created_at` int(1) unsigned NOT NULL,
  `modified_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;