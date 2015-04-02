/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50612
Source Host           : 127.0.0.1:3306
Source Database       : img_url

Target Server Type    : MYSQL
Target Server Version : 50612
File Encoding         : 65001

Date: 2015-04-03 05:28:17
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for url_json
-- ----------------------------
DROP TABLE IF EXISTS `url_json`;
CREATE TABLE `url_json` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT '2014-01-01 00:00:00' COMMENT '插入时间',
  `urls` mediumtext CHARACTER SET utf8 COMMENT 'json格式url地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
