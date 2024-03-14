-- https://stackoverflow.com/questions/36164338/design-database-for-multi-category-attribute

CREATE TABLE `products` (
  `product_id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

CREATE TABLE category (
    category_id INT(1) unsigned NOT NULL AUTO_INCREMENT,
    name varchar(45) NOT NULL,
    PRIMARY KEY(`category_id`),
    UNIQUE KEY category_index ('category_id','name')
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;