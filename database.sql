-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2413_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('1bf7841ca3a2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `fk_book_genre_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_book_genre_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_genre_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (12,1),(19,1),(20,1),(22,1),(22,2),(10,4),(11,4),(13,4),(14,4),(15,4),(16,4),(17,4),(18,5),(21,5);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `year` int(11) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `pages` int(11) NOT NULL,
  `cover_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_cover_id_covers` (`cover_id`),
  CONSTRAINT `fk_books_cover_id_covers` FOREIGN KEY (`cover_id`) REFERENCES `covers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (10,'Война и мир','<p>Исторический роман, описывающий события 1812 года и войны с Наполеоном.</p>\n',1869,'Русский Вестник','Лев Толстой',1225,10),(11,'Преступление и наказание','<p>Роман, в котором описывается <strong>внутренний мир</strong> и <strong>терзания убийцы</strong> и его путь к искуплению.</p>\n',1866,'Русский Вестник','Федор Достоевский',671,11),(12,'Мастер и Маргарита','<blockquote>\n  <p>Роман о визите дьявола в атеистический Советский Союз.</p>\n</blockquote>\n',1967,'Молодая гвардия','Михаил Булгаков',480,12),(13,'Анна Каренина','<p>Роман о <em>трагической судьбе женщины</em>, нарушившей социальные нормы.</p>\n',1878,'Русский Вестник','Лев Толстой',864,13),(14,'Братья Карамазовы','<p>Философский роман о конфликте между верой и безверием, а также о семейных драмах.</p>\n',1880,'Русский Вестник','Федор Достоевский',840,14),(15,'Идиот','<p>Роман о чистом человеке, которого жестокий мир делает <strong>идиотом</strong>.</p>\n',1869,'Русский Вестник','Федор Достоевский',736,15),(16,'Тихий Дон','<h1>Эпопея о жизни донских казаков в период революции и Гражданской войны в России.</h1>\n',1940,'Современник','Михаил Шолохов',1600,16),(17,'Евгений Онегин','<p><em>Классическое</em> произведение русской литературы, повествующее о жизни молодого дворянина.</p>\n',1833,'А.С. Пушкин','Александр Пушкин',224,17),(18,'Доктор Живаго','<p>Роман о жизни врача и поэта на фоне революции и Гражданской войны в России.</p>\n',1957,'Советский писатель','Борис Пастернак',592,18),(19,' Сталкер','<p><strong>Постапокалиптический</strong> роман о зоне, где происходят странные и опасные явления.</p>\n',1972,'Молодая гвардия','Аркадий и Борис Стругацкие',200,19),(20,'Ночной дозор','<p>Роман о борьбе света и тьмы в современном мире, где существуют <em>маги и оборотни</em>.</p>\n',1998,'АСТ','Сергей Лукьяненко',500,20),(21,'Чистый код','<p>Практическое руководство по написанию качественного кода и улучшению навыков <strong>программирования</strong>.</p>\n',2008,'Prentice Hall','Роберт Мартин',464,21),(22,'Повтор','<p>Проверка</p>\n',2024,' Neoclassic','sdfsdf',224,22);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_comments_book_id_books` (`book_id`),
  KEY `fk_comments_user_id_users` (`user_id`),
  CONSTRAINT `fk_comments_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_comments_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (9,10,'<p>УДАЧИ!</p>\n',1,5,'2024-06-15 13:15:55'),(10,21,'<p>Я практиковалась 3 месяца и получила хороший результат!</p>\n',3,4,'2024-06-15 14:35:17'),(11,10,'<p>Это очень тяжелая для меня книга :(</p>\n',3,2,'2024-06-15 14:37:08'),(12,20,'<p>Это просто <strong>шедевр</strong>!</p>\n',3,5,'2024-06-15 14:41:10'),(13,15,'<p>Идиот!</p>\n',3,5,'2024-06-15 15:09:42'),(14,19,'<p>Обожаю эту книгу!</p>\n',2,5,'2024-06-15 15:10:39'),(15,12,'<p>Что то ужасно <strong>непонятное</strong> происходит в этой книге....</p>\n',2,0,'2024-06-15 15:11:34'),(16,18,'<p>Берет за душу.</p>\n',2,4,'2024-06-15 15:11:57'),(17,20,'<p>Сомнительно, но окей.</p>\n',2,3,'2024-06-15 15:12:25'),(18,16,'<p>Захотелось  стать донским казаком!</p>\n',2,4,'2024-06-15 15:13:07'),(19,11,'<p>Эта книга на многое отокрыла мне глаза. Достоевский гений!</p>\n',2,5,'2024-06-15 15:13:45'),(20,17,'<p>Классика :)</p>\n',2,5,'2024-06-15 15:14:17'),(21,10,'<p>Все драмы пропускал, а вот про войну написано хорошо!</p>\n',2,4,'2024-06-15 15:15:07'),(22,21,'<p>Читала в запой!</p>\n',1,4,'2024-06-15 17:45:54');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (10,'война.jpg','image/jpeg','bb6df1b0242db9879f5337a37232e1c7'),(11,'преступление.jpg','image/jpeg','4d07ee6ae6a6f96ee45134c00e15b009'),(12,'мастер.jpeg','image/jpeg','012b25bff2c1d4a880916a5d4f9c3806'),(13,'анна.jpeg','image/jpeg','5c879e9a7a685d4424bf80b4d80c9ced'),(14,'братья.jpeg','image/jpeg','9d4807bf62e785ce69ec263c65a216ec'),(15,'идиот.jpeg','image/jpeg','bee850c91260366a2e36921ad0d0c06b'),(16,'дон.jpeg','image/jpeg','6ad086cb3067ca5ee148261080958a4f'),(17,'онегин.jpeg','image/jpeg','1ed079dc8d4cdf798e6940581f6f48b7'),(18,'доктор.jpeg','image/jpeg','2aafd2b860555d1a6cc9c54cfe8cc057'),(19,'сталкер.jpeg','image/jpeg','9e82d83a662345bae957bf25dd328972'),(20,'ночной д.jpeg','image/jpeg','54ba66ff4a3d8a874c4042c6cfc87647'),(21,'код.jpeg','image/jpeg','7a3923b5deda55843193c901bd7a47ad'),(22,'дон.jpeg','image/jpeg','6ad086cb3067ca5ee148261080958a4f');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (3,'Детектив'),(2,'Научная литература'),(1,'Приключения'),(4,'Роман'),(5,'Ужасы');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'moderator','Может редактировать данные книг и производить модерацию рецензий'),(3,'user','Может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Maria','0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e','Lesnikova','Maria','Ilinichna',1),(2,'Саша Микроб','cf7fea39f432968501615a11e9c487a64b135201487d8df33b82bbf5b4515fb1','Микробов','Саша',NULL,2),(3,'Мышонок','7f9bff2bb05cf147fbf9eca3343ced32ae9a84beecd2911099d154fe46dc8bb2','Мышкина','Юля',NULL,3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-16  0:06:34
