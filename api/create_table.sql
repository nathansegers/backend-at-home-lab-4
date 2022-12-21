CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` varchar(255) NOT NULL,
  `tools` text NULL,
  `semester` int NOT NULL,
  `weight` int NOT NULL,
  `pillar` varchar(255) NOT NULL,
  `track_id` int(11) NULL,
  `content` longtext NOT NULL,
  FOREIGN KEY (`track_id`) REFERENCES `tracks` (`id`) ON DELETE NO ACTION
);