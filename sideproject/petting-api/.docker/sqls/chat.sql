CREATE TABLE `chat_room` (
	`pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`nanoid` char(24) NOT NULL,
	`created_at` datetime NOT NULL,
  	`modified_at` datetime NOT NULL,
	PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `chat_room_member` (
	`pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`member_id` char(24) NOT NULL,
	`created_at` datetime NOT NULL,
  	`modified_at` datetime NOT NULL,
	PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `chat_request_history` (
	`pk` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`sender` char(24) NOT NULL COMMENT 'ref, member.nanoid',
	`receiver`char(24) NOT NULL COMMENT 'ref, member.nanoid',
	`status` varchar(12) NOT NULL,
	`created_at` datetime NOT NULL,
  	`modified_at` datetime NOT NULL,
  	PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;