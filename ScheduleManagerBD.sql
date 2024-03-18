DROP DATABASE IF EXISTS `MeetingScheduler` ;
CREATE DATABASE `MeetingScheduler` ;
USE `MeetingScheduler` ;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;


CREATE TABLE `rooms` (
`room_num` int(4) NOT NULL,
`capacity` int(11) NOT NULL,
PRIMARY KEY (`room_num`)
) ENGINE=InnoDB;

INSERT INTO `rooms` VALUES (100,30);

CREATE TABLE `meetings` (
`meeting_id` int(11) NOT NULL,
`meeting_time_start` int(11) NOT NULL,
`meeting_time_end` int(11) NOT NULL,
`room_num` int(4) NOT NULL,
`desc` varchar(100) NULL,
PRIMARY KEY (`meeting_id`),
KEY `fk_room_num` (`room_num`),
CONSTRAINT `fk_room_numx` FOREIGN KEY (`room_num`) REFERENCES `rooms` (`room_num`)
) ENGINE=InnoDB;

INSERT INTO `meetings` VALUES (1,'2000-01-01 22:00:00', '2000-01-01 23:00:00',100, 'This is a test');

CREATE TABLE `people` (
`people_id` int(11) NOT NULL,
`name` varchar(50) NOT NULL,
`isManager` bool DEFAULT 0,
`meeting_id` int(11) DEFAULT NULL,
`password` varchar(50) NOT NULL,
PRIMARY KEY (`people_id`),
KEY `fk_meeting_idxs` (`meeting_id`),
CONSTRAINT `fk_meeting_idxs` FOREIGN KEY (`meeting_id`) REFERENCES `meetings` (`meeting_id`)
) ENGINE=InnoDB;

INSERT INTO `people` VALUES (1,'default',1,1,'password');

CREATE TABLE `work_times` (
`work_time_id` int(11) NOT NULL,
`people_id` int(11) NOT NULL,
`date_time_start` datetime NOT NULL,
`date_time_end` datetime NOT NULL,
PRIMARY KEY (`work_time_id`),
KEY `fk_people_idx` (`people_id`),
CONSTRAINT `fk_people_idx` FOREIGN KEY (`people_id`) REFERENCES `people` (`people_id`)
) ENGINE=InnoDB;

INSERT INTO `work_times` VALUES (1,1,'2000-01-01 22:00:00', '2000-01-01 23:00:00');
