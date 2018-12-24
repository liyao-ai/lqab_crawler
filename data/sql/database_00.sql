
SET FOREIGN_KEY_CHECKS=0;

create database if not exists `lqab_basedata_a`  DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `lqab_basedata_a`;

/*Table structure for table `search_local_temp` */

DROP TABLE IF EXISTS `search_local_temp`;

CREATE TABLE `search_local_temp` (
  `uuid` varchar(36) NOT NULL COMMENT '唯一主键',
  `title` varchar(150) DEFAULT NULL COMMENT '文章标题',
  `url` varchar(2000) DEFAULT NULL COMMENT '文章地址',
  `summary` varchar(2000) DEFAULT NULL COMMENT '简介',
  `snapshot` varchar(2000) DEFAULT NULL COMMENT '快照地址',
  `img` varchar(2000) DEFAULT NULL COMMENT '图片地址',
  `shottime` varchar(50) DEFAULT NULL COMMENT '快照时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '本地录入时间',
  `create_user` varchar(50) DEFAULT 'wth' COMMENT '录入人',
  `search_keyword` varchar(200) DEFAULT NULL COMMENT '用户查询关键词',
  `search_plant` varchar(50) DEFAULT NULL COMMENT '采集的平台',
  PRIMARY KEY (`uuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `crawler_key`;

CREATE TABLE `crawler_key` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `note` varchar(128) NOT NULL DEFAULT 'n/a' COMMENT '密钥提示',
  `ckey` varchar(256) DEFAULT 'n/a' COMMENT '密钥',
  `v1` tinyint(255) DEFAULT '0' COMMENT '访问游标',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

