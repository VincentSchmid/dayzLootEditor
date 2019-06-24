-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: dayzitems
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `itemcombos`
--

DROP TABLE IF EXISTS `itemcombos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `itemcombos` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `item1` varchar(50) NOT NULL,
  `item2` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `item1` (`item1`),
  KEY `item2` (`item2`),
  CONSTRAINT `itemcombos_ibfk_1` FOREIGN KEY (`item1`) REFERENCES `items` (`name`),
  CONSTRAINT `itemcombos_ibfk_2` FOREIGN KEY (`item2`) REFERENCES `items` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=987 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `items` (
  `name` varchar(50) NOT NULL,
  `category` varchar(45) NOT NULL COMMENT 'weapons, tools, ... ',
  `type` varchar(45) DEFAULT NULL COMMENT 'Gun, Attachment, Ammo',
  `lifetime` int(11) unsigned NOT NULL,
  `quantmin` int(11) DEFAULT '-1',
  `nominal` int(11) unsigned DEFAULT '0',
  `cost` int(11) unsigned DEFAULT '100',
  `quantmax` int(11) NOT NULL DEFAULT '-1',
  `min` int(11) unsigned NOT NULL,
  `restock` int(11) unsigned NOT NULL,
  `Military` tinyint(1) unsigned zerofill NOT NULL,
  `Prison` tinyint(1) unsigned zerofill NOT NULL,
  `School` tinyint(1) unsigned zerofill NOT NULL,
  `Coast` tinyint(1) unsigned zerofill NOT NULL,
  `Village` tinyint(1) unsigned zerofill NOT NULL,
  `Industrial` tinyint(1) unsigned zerofill NOT NULL,
  `Medic` tinyint(1) unsigned zerofill NOT NULL,
  `Police` tinyint(1) unsigned zerofill NOT NULL,
  `Hunting` tinyint(1) unsigned zerofill NOT NULL,
  `Town` tinyint(1) unsigned zerofill NOT NULL,
  `Farm` tinyint(1) unsigned zerofill NOT NULL,
  `Firefighter` tinyint(1) unsigned zerofill NOT NULL,
  `Office` tinyint(1) unsigned zerofill NOT NULL,
  `Tier1` tinyint(1) unsigned zerofill NOT NULL,
  `Tier2` tinyint(1) unsigned zerofill NOT NULL,
  `Tier3` tinyint(1) unsigned zerofill NOT NULL,
  `Tier4` tinyint(1) unsigned zerofill NOT NULL,
  `shelves` tinyint(1) unsigned zerofill NOT NULL,
  `floor` tinyint(1) unsigned zerofill NOT NULL,
  `count_in_cargo` tinyint(1) unsigned zerofill NOT NULL,
  `count_in_hoarder` tinyint(1) unsigned zerofill NOT NULL,
  `count_in_map` tinyint(1) unsigned zerofill NOT NULL,
  `count_in_player` tinyint(1) unsigned zerofill NOT NULL,
  `crafted` tinyint(1) unsigned zerofill NOT NULL,
  `deloot` tinyint(1) unsigned zerofill NOT NULL,
  `ingameName` varchar(45) DEFAULT NULL,
  `rarity` tinyint(1) unsigned zerofill NOT NULL,
  `mod` varchar(25) NOT NULL DEFAULT 'Vanilla',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-24 18:47:56
