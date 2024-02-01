CREATE TABLE `products` (
  `product_id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE category (
    category_id INT(1) unsigned NOT NULL AUTO_INCREMENT,
    name varchar(45) NOT NULL,
    PRIMARY KEY(`category_id`),
    UNIQUE KEY category_index (`category_id`,`name`)
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE product_category (
    product_category_id INT(1) unsigned NOT NULL AUTO_INCREMENT,
    product_id INT(1) unsigned DEFAULT NULL,
    category_id INT(1) unsigned DEFAULT NULL,
    PRIMARY KEY(`product_category_id`),
    UNIQUE KEY product_category_index (`product_category_id`,`product_id`, `category_id`)
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;