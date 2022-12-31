CREATE DATABASE  IF NOT EXISTS `crawlingdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `crawlingdb`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: crawlingdb
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_rating_movie`
--

DROP TABLE IF EXISTS `user_rating_movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_rating_movie` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `movieID` bigint NOT NULL,
  `rated` int NOT NULL,
  `user_name` varchar(50) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `archived_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `moviedetails_for_user_rating` (`movieID`),
  CONSTRAINT `moviedetails_for_user_rating` FOREIGN KEY (`movieID`) REFERENCES `crawling_pagination_table_entertainment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_rating_movie`
--

LOCK TABLES `user_rating_movie` WRITE;
/*!40000 ALTER TABLE `user_rating_movie` DISABLE KEYS */;
INSERT INTO `user_rating_movie` VALUES (1,2,6,'dk899097','2022-12-03 10:43:11',NULL),(2,2,7,'dk899097','2022-12-03 10:43:40',NULL),(3,2,6,'dk899097','2022-12-05 23:17:13',NULL),(4,17,7,'dk899097','2022-12-05 23:33:35',NULL),(5,726,7,'dk899097','2022-12-11 21:30:39',NULL),(6,181,8,'dk899097','2022-12-11 21:31:04',NULL),(7,5,6,'dk899097','2022-12-25 01:56:15',NULL),(8,2,7,'dk899097','2022-12-26 22:17:03',NULL),(9,959,8,'dk899097','2022-12-30 21:24:20',NULL);
/*!40000 ALTER TABLE `user_rating_movie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-01  3:43:43
