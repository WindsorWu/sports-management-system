-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sports
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `announcement`
--

DROP TABLE IF EXISTS `announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `announcement_type` varchar(20) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `cover_image` varchar(100) DEFAULT NULL,
  `attachments` varchar(100) DEFAULT NULL,
  `is_published` tinyint(1) NOT NULL,
  `is_pinned` tinyint(1) NOT NULL,
  `view_count` int NOT NULL,
  `publish_time` datetime(6) DEFAULT NULL,
  `expire_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `event_id` bigint DEFAULT NULL,
  `summary` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `announcement_author_id_3ca64157_fk_user_id` (`author_id`),
  KEY `announcement_event_id_4d8f8552_fk_event_id` (`event_id`),
  KEY `announcemen_announc_1e1407_idx` (`announcement_type`),
  KEY `announcemen_is_publ_051df3_idx` (`is_published`,`publish_time` DESC),
  KEY `announcemen_is_pinn_d6ba68_idx` (`is_pinned` DESC),
  CONSTRAINT `announcement_author_id_3ca64157_fk_user_id` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `announcement_event_id_4d8f8552_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcement`
--

LOCK TABLES `announcement` WRITE;
/*!40000 ALTER TABLE `announcement` DISABLE KEYS */;
INSERT INTO `announcement` VALUES (5,'欢迎新用户','运动赛事是丰富大众课余生活、推动全民健身的重要载体，生命在于运动！','notice','normal','/images/announcements/announcement_20260201150315_0b9a746d.jpg','',1,1,1,'2026-02-01 07:03:22.616350',NULL,'2026-02-01 07:03:22.616635','2026-02-01 07:03:22.616639',1,NULL,'生命在于运动');
/*!40000 ALTER TABLE `announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 用户',6,'add_user'),(22,'Can change 用户',6,'change_user'),(23,'Can delete 用户',6,'delete_user'),(24,'Can view 用户',6,'view_user'),(25,'Can add 赛事',7,'add_event'),(26,'Can change 赛事',7,'change_event'),(27,'Can delete 赛事',7,'delete_event'),(28,'Can view 赛事',7,'view_event'),(29,'Can add 报名',8,'add_registration'),(30,'Can change 报名',8,'change_registration'),(31,'Can delete 报名',8,'delete_registration'),(32,'Can view 报名',8,'view_registration'),(33,'Can add 成绩',9,'add_result'),(34,'Can change 成绩',9,'change_result'),(35,'Can delete 成绩',9,'delete_result'),(36,'Can view 成绩',9,'view_result'),(37,'Can add 公告',10,'add_announcement'),(38,'Can change 公告',10,'change_announcement'),(39,'Can delete 公告',10,'delete_announcement'),(40,'Can view 公告',10,'view_announcement'),(41,'Can add 收藏',11,'add_favorite'),(42,'Can change 收藏',11,'change_favorite'),(43,'Can delete 收藏',11,'delete_favorite'),(44,'Can view 收藏',11,'view_favorite'),(45,'Can add 点赞',12,'add_like'),(46,'Can change 点赞',12,'change_like'),(47,'Can delete 点赞',12,'delete_like'),(48,'Can view 点赞',12,'view_like'),(49,'Can add 评论',13,'add_comment'),(50,'Can change 评论',13,'change_comment'),(51,'Can delete 评论',13,'delete_comment'),(52,'Can view 评论',13,'view_comment'),(53,'Can add 轮播图',14,'add_carousel'),(54,'Can change 轮播图',14,'change_carousel'),(55,'Can delete 轮播图',14,'delete_carousel'),(56,'Can view 轮播图',14,'view_carousel'),(57,'Can add 反馈',15,'add_feedback'),(58,'Can change 反馈',15,'change_feedback'),(59,'Can delete 反馈',15,'delete_feedback'),(60,'Can view 反馈',15,'view_feedback'),(61,'Can add 赛事任务',16,'add_eventassignment'),(62,'Can change 赛事任务',16,'change_eventassignment'),(63,'Can delete 赛事任务',16,'delete_eventassignment'),(64,'Can view 赛事任务',16,'view_eventassignment'),(65,'Can add 裁判赛事访问',17,'add_refereeeventaccess'),(66,'Can change 裁判赛事访问',17,'change_refereeeventaccess'),(67,'Can delete 裁判赛事访问',17,'delete_refereeeventaccess'),(68,'Can view 裁判赛事访问',17,'view_refereeeventaccess');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carousel`
--

DROP TABLE IF EXISTS `carousel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carousel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext,
  `image` varchar(500) NOT NULL,
  `link_url` varchar(200) DEFAULT NULL,
  `position` varchar(20) NOT NULL,
  `order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `click_count` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `creator_id` bigint NOT NULL,
  `event_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `carousel_creator_id_d30cd013_fk_user_id` (`creator_id`),
  KEY `carousel_event_id_4436bd27_fk_event_id` (`event_id`),
  KEY `carousel_positio_f35c9f_idx` (`position`,`is_active`,`order`),
  KEY `carousel_is_acti_5ff289_idx` (`is_active`),
  CONSTRAINT `carousel_creator_id_d30cd013_fk_user_id` FOREIGN KEY (`creator_id`) REFERENCES `user` (`id`),
  CONSTRAINT `carousel_event_id_4436bd27_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carousel`
--

LOCK TABLES `carousel` WRITE;
/*!40000 ALTER TABLE `carousel` DISABLE KEYS */;
INSERT INTO `carousel` VALUES (3,'欢迎',NULL,'/images/carousel/carousel_20260201150712_fc7c34b2.jpg','','home',0,1,NULL,NULL,0,'2026-02-01 07:07:18.443276','2026-02-01 07:07:18.443302',1,NULL);
/*!40000 ALTER TABLE `carousel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `content` longtext NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `like_count` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `content_type_id` int NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  `reply_to_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_reply_to_id_e983892a_fk_user_id` (`reply_to_id`),
  KEY `comment_content_3076b0_idx` (`content_type_id`,`object_id`),
  KEY `comment_user_id_bdf487_idx` (`user_id`),
  KEY `comment_parent__834718_idx` (`parent_id`),
  KEY `comment_created_0e639e_idx` (`created_at` DESC),
  CONSTRAINT `comment_content_type_id_142ac1c1_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `comment_parent_id_07748d21_fk_comment_id` FOREIGN KEY (`parent_id`) REFERENCES `comment` (`id`),
  CONSTRAINT `comment_reply_to_id_e983892a_fk_user_id` FOREIGN KEY (`reply_to_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_user_id_2224f9d1_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(10,'announcements','announcement'),(3,'auth','group'),(2,'auth','permission'),(14,'carousel','carousel'),(4,'contenttypes','contenttype'),(7,'events','event'),(16,'events','eventassignment'),(17,'events','refereeeventaccess'),(15,'feedback','feedback'),(13,'interactions','comment'),(11,'interactions','favorite'),(12,'interactions','like'),(8,'registrations','registration'),(9,'results','result'),(5,'sessions','session'),(6,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-30 10:20:38.886399'),(2,'contenttypes','0002_remove_content_type_name','2026-01-30 10:20:38.934226'),(3,'auth','0001_initial','2026-01-30 10:20:39.083933'),(4,'auth','0002_alter_permission_name_max_length','2026-01-30 10:20:39.116749'),(5,'auth','0003_alter_user_email_max_length','2026-01-30 10:20:39.122387'),(6,'auth','0004_alter_user_username_opts','2026-01-30 10:20:39.126003'),(7,'auth','0005_alter_user_last_login_null','2026-01-30 10:20:39.129623'),(8,'auth','0006_require_contenttypes_0002','2026-01-30 10:20:39.131586'),(9,'auth','0007_alter_validators_add_error_messages','2026-01-30 10:20:39.135115'),(10,'auth','0008_alter_user_username_max_length','2026-01-30 10:20:39.139006'),(11,'auth','0009_alter_user_last_name_max_length','2026-01-30 10:20:39.142342'),(12,'auth','0010_alter_group_name_max_length','2026-01-30 10:20:39.150953'),(13,'auth','0011_update_proxy_permissions','2026-01-30 10:20:39.154865'),(14,'auth','0012_alter_user_first_name_max_length','2026-01-30 10:20:39.158728'),(15,'users','0001_initial','2026-01-30 10:20:39.343779'),(16,'admin','0001_initial','2026-01-30 10:20:39.427973'),(17,'admin','0002_logentry_remove_auto_add','2026-01-30 10:20:39.433468'),(18,'admin','0003_logentry_add_action_flag_choices','2026-01-30 10:20:39.438813'),(19,'events','0001_initial','2026-01-30 10:20:39.454856'),(20,'announcements','0001_initial','2026-01-30 10:20:39.470847'),(21,'announcements','0002_initial','2026-01-30 10:20:39.591551'),(22,'carousel','0001_initial','2026-01-30 10:20:39.605633'),(23,'carousel','0002_initial','2026-01-30 10:20:39.723634'),(24,'events','0002_initial','2026-01-30 10:20:39.842875'),(25,'feedback','0001_initial','2026-01-30 10:20:39.894614'),(26,'feedback','0002_initial','2026-01-30 10:20:40.034598'),(27,'interactions','0001_initial','2026-01-30 10:20:40.145869'),(28,'interactions','0002_initial','2026-01-30 10:20:40.575524'),(29,'registrations','0001_initial','2026-01-30 10:20:40.635522'),(30,'registrations','0002_initial','2026-01-30 10:20:40.818015'),(31,'results','0001_initial','2026-01-30 10:20:40.881309'),(32,'results','0002_initial','2026-01-30 10:20:41.122786'),(33,'sessions','0001_initial','2026-01-30 10:20:41.146782'),(34,'carousel','0003_alter_carousel_image','2026-01-30 16:05:14.732156'),(35,'events','0003_alter_event_cover_image','2026-01-30 16:19:46.577309'),(36,'announcements','0003_add_summary','2026-02-01 04:07:03.125645'),(37,'events','0004_eventassignment','2026-02-01 10:18:49.675202'),(38,'events','0005_refereeeventaccess','2026-02-01 13:10:35.561153'),(39,'users','0002_alter_user_user_type','2026-02-01 13:41:07.529181');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('op892rupdey87oe60oecch6a6dbq8m7x','.eJxVjDsOwjAQBe_iGln-fyjpOYO13nVwANlSnFSIu0OkFNC-mXkvlmBba9pGWdJM7Mw0O_1uGfBR2g7oDu3WOfa2LnPmu8IPOvi1U3leDvfvoMKo3zrCFEipqAuhEz46b42fpJEUgrXeokf0UVpRXACThRSgImKQQjuUYNn7A8gsNu8:1vmPCD:WOY_mfagEYWFIJcOQ1_MrOr59tTeP9uhz-lD9B9bRZs','2026-02-15 04:36:25.205657');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `cover_image` varchar(500) DEFAULT NULL,
  `event_type` varchar(50) NOT NULL,
  `level` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `location` varchar(200) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `registration_start` datetime(6) NOT NULL,
  `registration_end` datetime(6) NOT NULL,
  `max_participants` int NOT NULL,
  `current_participants` int NOT NULL,
  `registration_fee` decimal(10,2) NOT NULL,
  `rules` longtext,
  `requirements` longtext,
  `prizes` longtext,
  `contact_person` varchar(50) NOT NULL,
  `contact_phone` varchar(11) NOT NULL,
  `contact_email` varchar(254) DEFAULT NULL,
  `view_count` int NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `organizer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_organizer_id_95964402_fk_user_id` (`organizer_id`),
  KEY `event_status_77ade7_idx` (`status`,`created_at` DESC),
  KEY `event_event_t_4c9c3b_idx` (`event_type`),
  KEY `event_start_t_a7590c_idx` (`start_time`),
  CONSTRAINT `event_organizer_id_95964402_fk_user_id` FOREIGN KEY (`organizer_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (5,'2026城市公益迷你马拉松大赛','本次赛事为公益性质迷你马拉松，赛程5公里，面向18-60周岁健康人群，无报名费，参赛选手可免费领取参赛包（含号码布、纪念T恤、饮用水）。赛事旨在倡导绿色健康生活理念，所有参赛选手完赛后可获得纪念奖牌，赛事报名费（无）及赞助款项将全部捐赠至本地公益健身项目。参赛需提前报名并提交健康承诺书，比赛当天请提前1小时到场签到，遵守赛事秩序，听从工作人员指引，禁止违规参赛。','/images/events/event_20260201161612_97776fa7.jpg','athletics','school','published','城市中央公园南门广场（起点）- 滨河绿道（终点）','2026-02-01 00:00:00.000000','2026-02-01 06:00:00.000000','2026-01-04 16:00:00.000000','2026-01-11 16:00:00.000000',0,3,0.00,NULL,NULL,NULL,'张老师','13902447042',NULL,13,0,'2026-02-01 08:16:15.928345','2026-02-01 08:55:16.673765',1);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_assignment`
--

DROP TABLE IF EXISTS `event_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_assignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `round_type` varchar(20) NOT NULL,
  `assigned_at` datetime(6) NOT NULL,
  `remarks` longtext,
  `assigned_by_id` bigint DEFAULT NULL,
  `event_id` bigint NOT NULL,
  `referee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_assignment_assigned_by_id_5062ec7e_fk_user_id` (`assigned_by_id`),
  KEY `event_assignment_event_id_10343d1f_fk_event_id` (`event_id`),
  KEY `event_assignment_referee_id_92488df2_fk_user_id` (`referee_id`),
  CONSTRAINT `event_assignment_assigned_by_id_5062ec7e_fk_user_id` FOREIGN KEY (`assigned_by_id`) REFERENCES `user` (`id`),
  CONSTRAINT `event_assignment_event_id_10343d1f_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `event_assignment_referee_id_92488df2_fk_user_id` FOREIGN KEY (`referee_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_assignment`
--

LOCK TABLES `event_assignment` WRITE;
/*!40000 ALTER TABLE `event_assignment` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorite`
--

DROP TABLE IF EXISTS `favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorite` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `content_type_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `favorite_user_id_content_type_id_object_id_ed90040d_uniq` (`user_id`,`content_type_id`,`object_id`),
  KEY `favorite_content_8de248_idx` (`content_type_id`,`object_id`),
  KEY `favorite_user_id_3c90f9_idx` (`user_id`),
  CONSTRAINT `favorite_content_type_id_0d75c052_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `favorite_user_id_8a5f8d2c_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `favorite_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite`
--

LOCK TABLES `favorite` WRITE;
/*!40000 ALTER TABLE `favorite` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `feedback_type` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `images` json DEFAULT NULL,
  `contact_info` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `reply` longtext,
  `handled_at` datetime(6) DEFAULT NULL,
  `is_anonymous` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `event_id` bigint DEFAULT NULL,
  `handler_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `feedback_event_id_c2447e92_fk_event_id` (`event_id`),
  KEY `feedback_handler_id_ea96a7d9_fk_user_id` (`handler_id`),
  KEY `feedback_status_711338_idx` (`status`,`created_at` DESC),
  KEY `feedback_feedbac_533c89_idx` (`feedback_type`),
  KEY `feedback_user_id_8cf53b_idx` (`user_id`),
  CONSTRAINT `feedback_event_id_c2447e92_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `feedback_handler_id_ea96a7d9_fk_user_id` FOREIGN KEY (`handler_id`) REFERENCES `user` (`id`),
  CONSTRAINT `feedback_user_id_0104a377_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `like`
--

DROP TABLE IF EXISTS `like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `like` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `content_type_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `like_user_id_content_type_id_object_id_c07adf35_uniq` (`user_id`,`content_type_id`,`object_id`),
  KEY `like_content_bc653d_idx` (`content_type_id`,`object_id`),
  KEY `like_user_id_8ed00c_idx` (`user_id`),
  CONSTRAINT `like_content_type_id_8424068b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `like_user_id_318aef4d_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `like_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `like`
--

LOCK TABLES `like` WRITE;
/*!40000 ALTER TABLE `like` DISABLE KEYS */;
/*!40000 ALTER TABLE `like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referee_event_access`
--

DROP TABLE IF EXISTS `referee_event_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referee_event_access` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `event_id` bigint NOT NULL,
  `referee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `referee_event_access_referee_id_event_id_552d82c9_uniq` (`referee_id`,`event_id`),
  KEY `referee_event_access_event_id_a8eb1eab_fk_event_id` (`event_id`),
  CONSTRAINT `referee_event_access_event_id_a8eb1eab_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `referee_event_access_referee_id_67db8669_fk_user_id` FOREIGN KEY (`referee_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referee_event_access`
--

LOCK TABLES `referee_event_access` WRITE;
/*!40000 ALTER TABLE `referee_event_access` DISABLE KEYS */;
INSERT INTO `referee_event_access` VALUES (4,'2026-02-01 15:04:01.069910',5,9);
/*!40000 ALTER TABLE `referee_event_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  `registration_number` varchar(50) NOT NULL,
  `participant_name` varchar(50) NOT NULL,
  `participant_phone` varchar(11) NOT NULL,
  `participant_id_card` varchar(18) NOT NULL,
  `participant_gender` varchar(1) NOT NULL,
  `participant_birth_date` date NOT NULL,
  `participant_organization` varchar(100) DEFAULT NULL,
  `emergency_contact` varchar(50) NOT NULL,
  `emergency_phone` varchar(11) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `payment_amount` decimal(10,2) NOT NULL,
  `payment_time` datetime(6) DEFAULT NULL,
  `remarks` longtext,
  `review_remarks` longtext,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `event_id` bigint NOT NULL,
  `reviewed_by_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  UNIQUE KEY `registration_event_id_user_id_078ef461_uniq` (`event_id`,`user_id`),
  KEY `registration_reviewed_by_id_61905c21_fk_user_id` (`reviewed_by_id`),
  KEY `registration_user_id_99fc0ecd_fk_user_id` (`user_id`),
  KEY `registratio_status_4e916b_idx` (`status`),
  KEY `registratio_registr_a600c8_idx` (`registration_number`),
  KEY `registratio_event_i_3fb224_idx` (`event_id`,`user_id`),
  CONSTRAINT `registration_event_id_94e1df59_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `registration_reviewed_by_id_61905c21_fk_user_id` FOREIGN KEY (`reviewed_by_id`) REFERENCES `user` (`id`),
  CONSTRAINT `registration_user_id_99fc0ecd_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (2,'approved','REG-5-20260201082151-2B61151A','张三','13725629630','51323219961104755X','M','1996-11-04','','张先生','15271972431','unpaid',0.00,NULL,'','','2026-02-01 08:23:55.967640','2026-02-01 08:21:51.654466','2026-02-01 08:23:55.967813',5,1,6),(3,'approved','REG-5-20260201082233-4326653B','李四','13913737767','50011419970105323X','M','1997-01-05','','李先生','13766921774','unpaid',0.00,NULL,'','','2026-02-01 08:23:57.404392','2026-02-01 08:22:33.323362','2026-02-01 08:23:57.404560',5,1,7),(4,'approved','REG-5-20260201082339-610DC4F5','王五','15298052283','650421199905310544','M','1999-05-31','城市实验中学','王先生','15246009563','unpaid',0.00,NULL,'','','2026-02-01 08:23:58.473829','2026-02-01 08:23:39.698131','2026-02-01 08:23:58.473994',5,1,8);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `round_type` varchar(20) NOT NULL,
  `score` varchar(100) NOT NULL,
  `rank` int DEFAULT NULL,
  `award` varchar(50) DEFAULT NULL,
  `score_unit` varchar(20) DEFAULT NULL,
  `remarks` longtext,
  `certificate_url` varchar(200) DEFAULT NULL,
  `is_published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `event_id` bigint NOT NULL,
  `recorded_by_id` bigint DEFAULT NULL,
  `registration_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `result_recorded_by_id_f3887c68_fk_user_id` (`recorded_by_id`),
  KEY `result_registration_id_e9a6919b_fk_registration_id` (`registration_id`),
  KEY `result_event_i_d78629_idx` (`event_id`,`rank`),
  KEY `result_user_id_8341d8_idx` (`user_id`),
  KEY `result_is_publ_42fa45_idx` (`is_published`),
  CONSTRAINT `result_event_id_db768a07_fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `result_recorded_by_id_f3887c68_fk_user_id` FOREIGN KEY (`recorded_by_id`) REFERENCES `user` (`id`),
  CONSTRAINT `result_registration_id_e9a6919b_fk_registration_id` FOREIGN KEY (`registration_id`) REFERENCES `registration` (`id`),
  CONSTRAINT `result_user_id_e5f79d30_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (4,'final','2:06:26',1,'冠军奖牌',NULL,NULL,NULL,1,'2026-02-01 09:18:00.772905','2026-02-01 09:18:00.772933',5,9,4,8),(5,'final','2:06:47',2,'亚军奖牌',NULL,NULL,NULL,1,'2026-02-01 09:18:20.970948','2026-02-01 09:18:20.970972',5,9,2,6),(6,'final','2:07:00',3,'季军奖牌',NULL,NULL,NULL,1,'2026-02-01 09:18:41.175933','2026-02-01 09:18:41.175955',5,9,3,7);
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `real_name` varchar(50) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `id_card` varchar(18) DEFAULT NULL,
  `emergency_contact` varchar(50) DEFAULT NULL,
  `emergency_phone` varchar(11) DEFAULT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `bio` longtext,
  `is_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `id_card` (`id_card`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'pbkdf2_sha256$720000$SBwadYvwrudwkQNHNazt84$fvr2fRUkkQp7konKjcvFWcNnrMh28jKSU37HfZ5HBGE=','2026-02-01 14:43:37.894806',1,'admin','','','admin@example.com',1,1,'2026-01-30 10:20:57.260005','管理员','13800138000','admin','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-30 10:20:57.490776','2026-01-30 10:20:57.490784'),(6,'pbkdf2_sha256$720000$rYzpMTOk7LdxEOUzIYQurD$v7P5bnYmejJ+9M8OE1hk3oNRHEjO9ha+OhZqEzBU0wY=','2026-02-01 09:33:24.536304',0,'ZhangSan','','','zhangsan@sports.cn',0,1,'2026-02-01 06:42:52.888912','张三','13725629630','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-02-01 06:42:53.122440','2026-02-01 06:42:53.122449'),(7,'pbkdf2_sha256$720000$UV1wPUvrXAwsNRF0ysaF8K$ku+AYt8aC7vx5g3aAhGKrK9XFKjXekZm0hAgAu4Kly0=','2026-02-01 08:22:07.111833',0,'LiSi','','','lisi@sports.cn',0,1,'2026-02-01 06:44:16.800421','李四','13913737767','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-02-01 06:44:17.144494','2026-02-01 06:44:17.144506'),(8,'pbkdf2_sha256$720000$Ds1AMrjPRJkaKgmF8MRiJ4$p+weEgnuK/xOUA5GK4+RlTQgVvD+HrTjU82WjCMpESc=','2026-02-01 08:22:43.809783',0,'WangWu','','','wangwu@sports.cn',0,1,'2026-02-01 06:44:59.968065','王五','15298052283','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-02-01 06:45:00.356992','2026-02-01 06:45:00.357010'),(9,'pbkdf2_sha256$720000$cDnmoOoZpkdaFME5wLXD1F$OAT6mzn3ApNCfhZd910akqS+f07GgNJBSxL9I2Fn+Uw=','2026-02-01 14:49:13.170676',0,'李寻欢','','','lixunhuan@sports.cn',1,1,'2026-02-01 08:49:52.906271','李寻欢','15210123318','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-02-01 08:49:53.134635','2026-02-01 10:47:04.577410');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_user_id_abaea130_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id_7dc6e2e0_uniq` (`user_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_permissions_user_id_ed4a47ea_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-01 23:22:48
