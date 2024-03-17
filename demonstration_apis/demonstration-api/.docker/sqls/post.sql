CREATE TABLE `posts` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `like` int(10) unsigned DEFAULT 0,
  `version` int(1) unsigned DEFAULT 0 NOT NULL,
  `modified_at` int(1) unsigned DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `post_comments` (
  `pk` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `post_id` int(1) unsigned NOT NULL,
  `created_at` int(1) unsigned DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
