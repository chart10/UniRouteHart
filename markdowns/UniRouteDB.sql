CREATE database IF NOT EXISTS UniRouteDB;

USE UniRouteDB;

CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(80) NOT NULL,
  `email` varchar(30) NOT NULL,
  `university` varchar(30) DEFAULT NULL,
  `firstName` varchar(30) DEFAULT NULL,
  `lastName` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `password` (`password`)
);

CREATE TABLE IF NOT EXISTS `addresses` (
  `username` varchar(30) NOT NULL,
  `addressID` int NOT NULL AUTO_INCREMENT,
  `address` varchar(40) NOT NULL,
  `addressType` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`username`,`addressID`),
  UNIQUE KEY `addressID` (`addressID`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `phoneNumbers` (
  `username` varchar(30) NOT NULL,
  `phoneID` int NOT NULL AUTO_INCREMENT,
  `phoneNumber` varchar(20) NOT NULL,
  `phoneType` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`username`,`phoneID`),
  UNIQUE KEY `phoneID` (`phoneID`),
  CONSTRAINT `phonenumbers_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `recentRoutes` (
  `username` varchar(30) NOT NULL,
  `routeID` int NOT NULL AUTO_INCREMENT,
  `departAddress` varchar(40) DEFAULT NULL,
  `arriveAddress` varchar(40) NOT NULL,
  `dateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`username`,`routeID`),
  UNIQUE KEY `routeID` (`routeID`),
  CONSTRAINT `recentroutes_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `scheduledRoutes` (
  `username` varchar(30) NOT NULL,
  `routeID` int NOT NULL AUTO_INCREMENT,
  `departArrive` enum('DEPART','ARRIVE') DEFAULT NULL,
  `timeOfDay` time DEFAULT NULL,
  `origin` varchar(40) DEFAULT NULL,
  `destination` varchar(40) NOT NULL,
  `travelMode` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`username`,`routeID`),
  UNIQUE KEY `routeID` (`routeID`),
  CONSTRAINT `scheduledroutes_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `scheduledRoutesDayOfWeek` (
  `routeID` int NOT NULL,
  `subID` int NOT NULL AUTO_INCREMENT,
  `dayOfWeek` tinyint NOT NULL,
  PRIMARY KEY (`routeID`,`subID`),
  UNIQUE KEY `subID` (`subID`),
  CONSTRAINT `scheduledroutesdayofweek_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `scheduledRoutes` (`routeID`) ON DELETE CASCADE ON UPDATE CASCADE
);