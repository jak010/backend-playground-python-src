CREATE TABLE `submissions` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `audition_id` int(1) unsigned NOT NULL COMMENT 'auditions .auditions_id',
  `member_id` char(36) NOT NULL COMMENT '`member`.member_id',
  `status` varchar(32) DEFAULT NULL,
  `created_at` int(1) unsigned NOT NULL,
  `modified_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `submission_index` (`audition_id`,`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;