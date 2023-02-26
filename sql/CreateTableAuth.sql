CREATE TABLE IF NOT EXISTS `auth` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`User ID` INT NOT NULL,
	`Code` VARCHAR(50) NOT NULL,
	`Expires` TIMESTAMP NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `FK_users` FOREIGN KEY (`User ID`) REFERENCES `users` (`id`) ON DELETE CASCADE
);