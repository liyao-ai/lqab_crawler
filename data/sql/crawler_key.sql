/*
Navicat MySQL Data Transfer

Source Server         : lqab
Source Server Version : 50625
Source Host           : localhost:3306
Source Database       : lqab_basedata_a

Target Server Type    : MYSQL
Target Server Version : 50625
File Encoding         : 65001

Date: 2018-12-14 09:59:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for crawler_key
-- ----------------------------
DROP TABLE IF EXISTS `crawler_key`;
CREATE TABLE `crawler_key` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `note` varchar(128) NOT NULL DEFAULT 'n/a' COMMENT '密钥提示',
  `ckey` varchar(256) DEFAULT 'n/a' COMMENT '密钥',
  `v1` tinyint(255) DEFAULT '0' COMMENT '访问游标',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of crawler_key
-- ----------------------------
INSERT INTO `crawler_key` VALUES ('1', '一切分析都是可以计算的！', 'fbc37fe869960998c7da80da4e936ad2', '0');
INSERT INTO `crawler_key` VALUES ('2', '不加密的传输二不二？', 'n/a', '0');
INSERT INTO `crawler_key` VALUES ('3', '大头大头', 'd9217d2820e6ae2a4afeffd4cd63b860', '0');
INSERT INTO `crawler_key` VALUES ('4', 'n/a', 'e5b86d6784cd5d18e39ab6b705f09ebf', '0');
INSERT INTO `crawler_key` VALUES ('5', ' ', '8a80a26ef696a259fc618f5288dbf44c', '0');
