CREATE TABLE `verification` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `sender` varchar(128) NOT NULL,
  `receiver` varchar(128) NOT NULL,
  `code` char(6) NOT NULL,
  `type` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL COMMENT '0:전송, 1:인증완료, 2:인증파기',
  `expired_at` int(1) unsigned NOT NULL,
  `created_at` int(1) unsigned NOT NULL,
  `modified_at` int(1) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8