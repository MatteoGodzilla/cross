CREATE DATABASE IF NOT EXISTS `cross`;

USE `cross`;

CREATE TABLE IF NOT EXISTS `customs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `IDTag` varchar(50) NOT NULL,
  `BPM` float DEFAULT 120,
  `DownloadLink` longtext DEFAULT NULL,
  `Name1` varchar(50) DEFAULT NULL,
  `Artist1` varchar(50) DEFAULT NULL,
  `Name2` varchar(50) DEFAULT NULL,
  `Artist2` varchar(50) DEFAULT NULL,
  `Name3` varchar(50) DEFAULT NULL,
  `Artist3` varchar(50) DEFAULT NULL,
  `Charter` varchar(50) DEFAULT NULL,
  `Mixer` varchar(50) DEFAULT NULL,
  `DiffGeneral` tinyint(8) unsigned DEFAULT 0,
  `DiffTap` tinyint(8) unsigned DEFAULT 0,
  `DiffCrossfade` tinyint(8) unsigned DEFAULT 0,
  `DiffScratch` tinyint(8) unsigned DEFAULT 0,
  `HasBeginnerChart` tinyint(1) DEFAULT 0,
  `HasEasyChart` tinyint(1) DEFAULT 0,
  `HasMediumChart` tinyint(1) DEFAULT 0,
  `HasHardChart` tinyint(1) DEFAULT 0,
  `HasExpertChart` tinyint(1) DEFAULT 0,
  `DeckSpeedBeginner` float DEFAULT 1,
  `DeckSpeedEasy` float DEFAULT 1,
  `DeckSpeedMedium` float DEFAULT 1,
  `DeckSpeedHard` float DEFAULT 1,
  `DeckSpeedExpert` float DEFAULT 1,
  `VideoLink` longtext DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  `visible` tinyint(1) DEFAULT 1,
  `lastUpdate` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `IDTag_UNIQUE` (`IDTag`)
);
