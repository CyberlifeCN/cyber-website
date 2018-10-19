REPLACE INTO mysql.user (Host, User, Password) VALUES('localhost', 'cyber', password('cyber') );
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS cyber;
GRANT ALL PRIVILEGES ON cyber.* TO cyber@localhost IDENTIFIED BY 'cyber';
FLUSH PRIVILEGES;

USE cyber;

CREATE TABLE IF NOT EXISTS `article` (
  `_id` char(32) NOT NULL COMMENT 'uuid',
  `ctime` bigint(19) NOT NULL DEFAULT '0',
  `mtime` bigint(19) NOT NULL DEFAULT '0',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `category` (
  `_id` char(32) NOT NULL COMMENT 'uuid',
  `name` varchar(255) DEFAULT NULL,
  `ctime` bigint(19) NOT NULL DEFAULT '0',
  `mtime` bigint(19) NOT NULL DEFAULT '0',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `article_categories` (
  `article_id` char(32) NOT NULL COMMENT 'uuid',
  `category_id` char(32) NOT NULL COMMENT 'uuid',
  `ctime` bigint(19) NOT NULL DEFAULT '0',
  `mtime` bigint(19) NOT NULL DEFAULT '0',
  PRIMARY KEY (`article_id`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
