CREATE TABLE legacy_users (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL,
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `legacy_campaigns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `budget` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE legacy_adgroup (
  id INT AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  campaign_id INT NOT NULL,
  user_id INT NOT NULL,
  link_url VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  deleted_at DATETIME,
  PRIMARY KEY (id)
) ENGINE=InnoDB CHARACTER SET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE legacy_keyword (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    adgroup_id INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
) ENGINE=InnoDB CHARACTER SET=utf8 COLLATE=utf8_unicode_ci;