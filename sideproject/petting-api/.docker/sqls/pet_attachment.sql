CREATE TABLE `pet_attachment` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nanoid` char(24) NOT NULL COMMENT 'ref, pet.nanoid',
  `member_id` char(24) NOT NULL COMMENT 'ref, member.nanoid',
  `attachment_type` varchar(12) NOT NULL,
  `attachment_label` varchar(12) NOT NULL,
  `s3_key` varchar(512) DEFAULT NULL COMMENT 's3, saved key',
  `file_name` varchar(64) NOT NULL COMMENT 's3, file_name',
  `file_size` int(1) unsigned NOT NULL,
  `content_type` varchar(64) NOT NULL COMMENT 'content_type',
  `created_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`pk`),
  UNIQUE KEY `pet_attachment_indexer_1` (`member_id`,`file_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8