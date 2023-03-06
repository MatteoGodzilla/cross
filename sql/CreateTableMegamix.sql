CREATE TABLE IF NOT EXISTS `megamix` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `Name` varchar(50) DEFAULT NULL,
    `DownloadLink` longtext DEFAULT NULL,
    `VideoPreview` longtext DEFAULT NULL,
    `lastUpdate` TIMESTAMP NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `megamix-customs`(
    `megamixID` int(11) NOT NULL,
    `customID` int(11) NOT NULL,
    `order` smallint NOT NULL,
    FOREIGN KEY(`megamixID`) REFERENCES `megamix`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`customID`) REFERENCES `customs`(`id`) ON DELETE CASCADE
);