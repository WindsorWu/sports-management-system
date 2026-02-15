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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcement`
--

LOCK TABLES `announcement` WRITE;
/*!40000 ALTER TABLE `announcement` DISABLE KEYS */;
INSERT INTO `announcement` (`id`, `title`, `content`, `announcement_type`, `priority`, `cover_image`, `attachments`, `is_published`, `is_pinned`, `view_count`, `publish_time`, `expire_time`, `created_at`, `updated_at`, `author_id`, `event_id`, `summary`) VALUES (5,'欢迎新用户','运动赛事是丰富大众课余生活、推动全民健身的重要载体，生命在于运动！','notice','normal','/images/announcements/announcement_20260201150315_0b9a746d.jpg','',1,1,1,'2026-02-01 07:03:22.616350',NULL,'2026-02-01 07:03:22.616635','2026-02-01 07:03:22.616639',1,NULL,'生命在于运动'),(6,'新赛事正在进行中','欢迎观赛','notice','normal','/images/announcements/announcement_20260215152218_bf874420.jpg','',1,0,1,'2026-02-15 07:22:28.354456',NULL,'2026-02-15 07:22:25.642633','2026-02-15 07:22:28.354669',1,NULL,'新赛事正在进行中');
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
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 用户',6,'add_user'),(22,'Can change 用户',6,'change_user'),(23,'Can delete 用户',6,'delete_user'),(24,'Can view 用户',6,'view_user'),(25,'Can add 赛事',7,'add_event'),(26,'Can change 赛事',7,'change_event'),(27,'Can delete 赛事',7,'delete_event'),(28,'Can view 赛事',7,'view_event'),(29,'Can add 报名',8,'add_registration'),(30,'Can change 报名',8,'change_registration'),(31,'Can delete 报名',8,'delete_registration'),(32,'Can view 报名',8,'view_registration'),(33,'Can add 成绩',9,'add_result'),(34,'Can change 成绩',9,'change_result'),(35,'Can delete 成绩',9,'delete_result'),(36,'Can view 成绩',9,'view_result'),(37,'Can add 公告',10,'add_announcement'),(38,'Can change 公告',10,'change_announcement'),(39,'Can delete 公告',10,'delete_announcement'),(40,'Can view 公告',10,'view_announcement'),(41,'Can add 收藏',11,'add_favorite'),(42,'Can change 收藏',11,'change_favorite'),(43,'Can delete 收藏',11,'delete_favorite'),(44,'Can view 收藏',11,'view_favorite'),(45,'Can add 点赞',12,'add_like'),(46,'Can change 点赞',12,'change_like'),(47,'Can delete 点赞',12,'delete_like'),(48,'Can view 点赞',12,'view_like'),(49,'Can add 评论',13,'add_comment'),(50,'Can change 评论',13,'change_comment'),(51,'Can delete 评论',13,'delete_comment'),(52,'Can view 评论',13,'view_comment'),(53,'Can add 轮播图',14,'add_carousel'),(54,'Can change 轮播图',14,'change_carousel'),(55,'Can delete 轮播图',14,'delete_carousel'),(56,'Can view 轮播图',14,'view_carousel'),(57,'Can add 反馈',15,'add_feedback'),(58,'Can change 反馈',15,'change_feedback'),(59,'Can delete 反馈',15,'delete_feedback'),(60,'Can view 反馈',15,'view_feedback'),(61,'Can add 赛事任务',16,'add_eventassignment'),(62,'Can change 赛事任务',16,'change_eventassignment'),(63,'Can delete 赛事任务',16,'delete_eventassignment'),(64,'Can view 赛事任务',16,'view_eventassignment'),(65,'Can add 裁判赛事访问',17,'add_refereeeventaccess'),(66,'Can change 裁判赛事访问',17,'change_refereeeventaccess'),(67,'Can delete 裁判赛事访问',17,'delete_refereeeventaccess'),(68,'Can view 裁判赛事访问',17,'view_refereeeventaccess');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carousel`
--

LOCK TABLES `carousel` WRITE;
/*!40000 ALTER TABLE `carousel` DISABLE KEYS */;
INSERT INTO `carousel` (`id`, `title`, `description`, `image`, `link_url`, `position`, `order`, `is_active`, `start_time`, `end_time`, `click_count`, `created_at`, `updated_at`, `creator_id`, `event_id`) VALUES (3,'欢迎',NULL,'/images/carousel/carousel_20260201150712_fc7c34b2.jpg','','home',0,1,NULL,NULL,0,'2026-02-01 07:07:18.443276','2026-02-01 07:07:18.443302',1,NULL),(4,'围棋',NULL,'/images/carousel/carousel_20260215152238_b2c70371.jpg','http://localhost:5173/events/13','home',1,1,NULL,NULL,0,'2026-02-15 07:22:52.963892','2026-02-15 07:22:52.963918',1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` (`id`, `object_id`, `content`, `is_approved`, `like_count`, `created_at`, `updated_at`, `content_type_id`, `parent_id`, `reply_to_id`, `user_id`) VALUES (4,5,'2026 城市公益迷你马拉松圆满落幕✨ 作为参赛的选手，全程被温暖与热爱包围！3 公里的赛道串联起城市的烟火与风光，补给站的温水、志愿者的贴心指引、沿途市民的呐喊加油，每一处细节都藏着主办方的用心。最有意义的不是冲线的瞬间，而是知道自己每跑一步，都在为公益添一份力 —— 这场奔跑，无关速度，只关善意。马年伊始，以奔跑赴热爱，以微光聚暖流，愿明年继续与这场有温度的赛事相遇，和更多人一起，用脚步传递力量，用善意点亮城市❤️',1,0,'2026-02-02 13:51:03.529553','2026-02-02 13:51:03.529578',7,NULL,NULL,8),(5,5,'5 公里的距离刚刚好，无报名费还能领参赛包，跑完全程既锻炼了身体，还能为本地公益健身项目出份力，太有意义了！',1,0,'2026-02-03 07:43:29.367362','2026-02-03 07:43:29.367378',7,NULL,NULL,6),(6,5,'第一次参加公益迷你马，赛事组织超棒，签到有序，工作人员指引也很清晰，全程体验感拉满～',1,0,'2026-02-03 07:45:32.728607','2026-02-03 07:45:32.728622',7,NULL,NULL,7),(7,5,'和朋友一起冲线的感觉太爽了！完赛奖牌质感超赞，更开心的是所有赞助都能捐给本地公益，奔跑的每一步都有价值。',1,0,'2026-02-03 07:45:59.364897','2026-02-03 07:45:59.364911',7,NULL,NULL,27),(8,5,'不用花一分钱，有纪念 T 恤、饮用水，完赛还有奖牌，这样的公益赛事请多办几场，下次必来！',1,0,'2026-02-03 07:46:27.146544','2026-02-03 07:46:27.146558',7,NULL,NULL,19),(9,5,'整场比赛氛围超棒，大家相互鼓励，既践行了绿色健康的理念，又做了公益，身心都超舒畅。',1,0,'2026-02-03 07:46:52.335795','2026-02-03 07:46:52.335811',7,NULL,NULL,13),(10,5,'参赛包的纪念 T 恤设计很有城市特色，饮用水补给也很到位，5 公里跑下来一点都不累，超享受这个过程。',1,0,'2026-02-03 07:48:13.077953','2026-02-03 07:48:13.077978',7,NULL,NULL,100),(11,5,'提交健康承诺书这个环节特别贴心，赛事方很重视参赛者的健康，细节真的拉满了。',1,0,'2026-02-03 07:48:30.423248','2026-02-03 07:48:30.423264',7,NULL,NULL,98),(12,5,'为绿色健康奔跑，为本地公益助力，跑完全程拿到奖牌的那一刻，成就感直接拉满！',1,0,'2026-02-03 07:48:51.153410','2026-02-03 07:48:51.153434',7,NULL,NULL,97),(13,5,'平时就喜欢慢跑，这次借着公益迷你马的机会，既运动又做了好事，收获双倍快乐～',1,0,'2026-02-03 07:49:16.435442','2026-02-03 07:49:16.435480',7,NULL,NULL,96),(14,5,'本来只是抱着试试看的心态报名，结果被这场公益迷你马圈粉了，流程顺畅，福利满满，公益初心更动人。',1,0,'2026-02-03 07:49:34.715689','2026-02-03 07:49:34.715703',7,NULL,NULL,95),(15,5,'全程跑下来沿途的风景也超美，一边慢跑一边感受城市风光，还能参与公益，简直太美好了。',1,0,'2026-02-03 07:51:07.114831','2026-02-03 07:51:07.114845',7,NULL,NULL,93),(16,5,'践行绿色健康生活，原来可以这么简单，一场迷你马，让运动和公益完美结合，爱了爱了',1,0,'2026-02-03 07:51:24.768382','2026-02-03 07:51:24.768396',7,NULL,NULL,91),(17,5,'不用报名费，还能免费领物资、拿奖牌，更重要的是能助力本地公益健身，这样的好事必须支持！',1,0,'2026-02-03 07:51:44.379378','2026-02-03 07:51:44.379392',7,NULL,NULL,89);
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
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1,'admin','logentry'),(10,'announcements','announcement'),(3,'auth','group'),(2,'auth','permission'),(14,'carousel','carousel'),(4,'contenttypes','contenttype'),(7,'events','event'),(16,'events','eventassignment'),(17,'events','refereeeventaccess'),(15,'feedback','feedback'),(13,'interactions','comment'),(11,'interactions','favorite'),(12,'interactions','like'),(8,'registrations','registration'),(9,'results','result'),(5,'sessions','session'),(6,'users','user');
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'contenttypes','0001_initial','2026-01-30 10:20:38.886399'),(2,'contenttypes','0002_remove_content_type_name','2026-01-30 10:20:38.934226'),(3,'auth','0001_initial','2026-01-30 10:20:39.083933'),(4,'auth','0002_alter_permission_name_max_length','2026-01-30 10:20:39.116749'),(5,'auth','0003_alter_user_email_max_length','2026-01-30 10:20:39.122387'),(6,'auth','0004_alter_user_username_opts','2026-01-30 10:20:39.126003'),(7,'auth','0005_alter_user_last_login_null','2026-01-30 10:20:39.129623'),(8,'auth','0006_require_contenttypes_0002','2026-01-30 10:20:39.131586'),(9,'auth','0007_alter_validators_add_error_messages','2026-01-30 10:20:39.135115'),(10,'auth','0008_alter_user_username_max_length','2026-01-30 10:20:39.139006'),(11,'auth','0009_alter_user_last_name_max_length','2026-01-30 10:20:39.142342'),(12,'auth','0010_alter_group_name_max_length','2026-01-30 10:20:39.150953'),(13,'auth','0011_update_proxy_permissions','2026-01-30 10:20:39.154865'),(14,'auth','0012_alter_user_first_name_max_length','2026-01-30 10:20:39.158728'),(15,'users','0001_initial','2026-01-30 10:20:39.343779'),(16,'admin','0001_initial','2026-01-30 10:20:39.427973'),(17,'admin','0002_logentry_remove_auto_add','2026-01-30 10:20:39.433468'),(18,'admin','0003_logentry_add_action_flag_choices','2026-01-30 10:20:39.438813'),(19,'events','0001_initial','2026-01-30 10:20:39.454856'),(20,'announcements','0001_initial','2026-01-30 10:20:39.470847'),(21,'announcements','0002_initial','2026-01-30 10:20:39.591551'),(22,'carousel','0001_initial','2026-01-30 10:20:39.605633'),(23,'carousel','0002_initial','2026-01-30 10:20:39.723634'),(24,'events','0002_initial','2026-01-30 10:20:39.842875'),(25,'feedback','0001_initial','2026-01-30 10:20:39.894614'),(26,'feedback','0002_initial','2026-01-30 10:20:40.034598'),(27,'interactions','0001_initial','2026-01-30 10:20:40.145869'),(28,'interactions','0002_initial','2026-01-30 10:20:40.575524'),(29,'registrations','0001_initial','2026-01-30 10:20:40.635522'),(30,'registrations','0002_initial','2026-01-30 10:20:40.818015'),(31,'results','0001_initial','2026-01-30 10:20:40.881309'),(32,'results','0002_initial','2026-01-30 10:20:41.122786'),(33,'sessions','0001_initial','2026-01-30 10:20:41.146782'),(34,'carousel','0003_alter_carousel_image','2026-01-30 16:05:14.732156'),(35,'events','0003_alter_event_cover_image','2026-01-30 16:19:46.577309'),(36,'announcements','0003_add_summary','2026-02-01 04:07:03.125645'),(37,'events','0004_eventassignment','2026-02-01 10:18:49.675202'),(38,'events','0005_refereeeventaccess','2026-02-01 13:10:35.561153'),(39,'users','0002_alter_user_user_type','2026-02-01 13:41:07.529181'),(40,'users','0003_allow_any_username_chars','2026-02-02 13:01:04.752485');
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
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES ('op892rupdey87oe60oecch6a6dbq8m7x','.eJxVjDsOwjAQBe_iGln-fyjpOYO13nVwANlSnFSIu0OkFNC-mXkvlmBba9pGWdJM7Mw0O_1uGfBR2g7oDu3WOfa2LnPmu8IPOvi1U3leDvfvoMKo3zrCFEipqAuhEz46b42fpJEUgrXeokf0UVpRXACThRSgImKQQjuUYNn7A8gsNu8:1vmPCD:WOY_mfagEYWFIJcOQ1_MrOr59tTeP9uhz-lD9B9bRZs','2026-02-15 04:36:25.205657');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` (`id`, `title`, `description`, `cover_image`, `event_type`, `level`, `status`, `location`, `start_time`, `end_time`, `registration_start`, `registration_end`, `max_participants`, `current_participants`, `registration_fee`, `rules`, `requirements`, `prizes`, `contact_person`, `contact_phone`, `contact_email`, `view_count`, `is_featured`, `created_at`, `updated_at`, `organizer_id`) VALUES (5,'2026城市公益迷你马拉松大赛','本次赛事为公益性质迷你马拉松，赛程5公里，面向18-60周岁健康人群，无报名费，参赛选手可免费领取参赛包（含号码布、纪念T恤、饮用水）。赛事旨在倡导绿色健康生活理念，所有参赛选手完赛后可获得纪念奖牌，赛事报名费（无）及赞助款项将全部捐赠至本地公益健身项目。参赛需提前报名并提交健康承诺书，比赛当天请提前1小时到场签到，遵守赛事秩序，听从工作人员指引，禁止违规参赛。','/images/events/event_20260201161612_97776fa7.jpg','田径','school','published','城市中央公园南门广场（起点）- 滨河绿道（终点）','2026-02-01 00:00:00.000000','2026-02-01 06:00:00.000000','2026-01-04 16:00:00.000000','2026-01-15 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'张老师','13902447042',NULL,78,0,'2026-02-01 08:16:15.928345','2026-02-03 13:46:09.762530',1),(6,'2026 城市公益篮球 3v3 挑战赛','面向 18-45 周岁人群，无报名费，参赛队可免费领取定制队服、饮用水。赛事旨在推广全民篮球运动，所有赞助款项将捐赠至老旧社区篮球场翻新项目。完赛队伍均可获得公益纪念证书，冠亚季军额外获得奖杯及运动装备。','/images/events/event_20260215124910_6f0c66b0.jpg','篮球','school','published','城市体育中心室外篮球场','2026-01-15 01:00:00.000000','2026-01-15 09:00:00.000000','2025-12-19 16:00:00.000000','2025-12-04 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'郑老师','15271807507',NULL,0,0,'2026-02-03 14:32:30.696663','2026-02-15 04:51:26.058134',1),(7,'城市绿道公益骑行挑战赛','面向 16-60 周岁健康人群，无报名费，参赛者可免费领取骑行头盔、补给包。赛事倡导绿色出行理念，所有赞助款项将捐赠至城市绿道维护及公益骑行驿站建设项目。完赛者可获得纪念奖牌及环保骑行徽章。','/images/events/event_20260215124729_65298846.jpg','骑行','school','published','城市中央公园北门（起点）- 生态湿地公园（终点）','2026-04-20 00:30:00.000000','2026-04-20 04:30:00.000000','2026-04-20 00:30:00.000000','2026-04-09 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'吴老师','13746980832',NULL,0,0,'2026-02-03 14:33:52.194890','2026-02-15 04:51:10.939516',1),(8,'亲子公益趣味定向赛','面向 4-12 岁儿童及家长组成的亲子家庭，无报名费，参赛家庭可免费领取任务包、亲子 T 恤。赛事旨在促进亲子互动与儿童运动习惯养成，所有赞助款项将捐赠至乡村学校儿童公益健身设施项目。完赛家庭可获得亲子纪念奖牌及儿童运动礼包。','/images/events/event_20260215124449_f02fc12e.jpg','田径','school','published','城市中央公园','2026-05-11 01:00:00.000000','2026-05-11 04:00:00.000000','2026-04-14 16:00:00.000000','2026-05-04 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'周先生','15229574574',NULL,0,0,'2026-02-03 14:34:37.502504','2026-02-15 04:50:56.255997',1),(9,'社区公益羽毛球团体赛','面向 18-55 周岁社区居民，无报名费，参赛队可免费领取运动毛巾、饮用水。赛事旨在丰富社区文体生活，所有赞助款项将捐赠至社区老年健身中心器材更新项目。完赛队伍均可获得公益纪念证书，冠军队获得专业羽毛球装备套装。','/images/events/event_20260215124316_7d029414.jpg','羽毛球','school','published','市民活动中心羽毛球馆','2026-06-14 06:00:00.000000','2026-06-15 09:00:00.000000','2026-05-19 16:00:00.000000','2026-06-04 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'李先生','13733579414',NULL,0,0,'2026-02-03 14:35:26.655022','2026-02-15 04:50:44.270105',1),(10,'城市公益徒步公益行','面向 18-65 周岁健康人群，无报名费，参赛者可免费领取防晒帽、补给包。赛事旨在倡导户外健康生活与生态保护，所有赞助款项将捐赠至城市河道生态保护公益项目。完赛者可获得纪念奖牌及环保主题周边。','/images/events/event_20260215122557_4c69a5f0.jpg','田径','school','published','城市滨江广场（起点）- 郊野公园（终点）','2026-07-05 00:00:00.000000','2026-07-05 08:00:00.000000','2026-06-09 16:00:00.000000','2026-06-24 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'孙老师','13912174257',NULL,2,0,'2026-02-03 14:36:18.674508','2026-02-15 04:50:34.370447',1),(11,'银发公益乒乓球友谊赛','面向 50-70 周岁中老年人群，无报名费，参赛者可免费领取防滑护具、饮用水。赛事旨在关爱中老年健康，所有赞助款项将捐赠至社区老年活动室器材升级项目。完赛者均可获得公益纪念证书及健康礼包，冠亚季军获得专业乒乓球拍套装。','/images/events/event_20260215122133_f09529d7.jpg','乒乓球','school','published','老年活动中心乒乓球馆','2026-08-23 01:00:00.000000','2026-08-24 08:00:00.000000','2026-07-24 16:00:00.000000','2026-08-14 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'钱女士','13940958322',NULL,2,0,'2026-02-03 14:36:46.131739','2026-02-15 04:50:22.641641',1),(12,'青年公益飞盘趣味赛','面向 18-35 周岁青年人群，无报名费，参赛队可免费领取飞盘、速干头巾。赛事旨在推广潮流运动与青年社交，所有赞助款项将捐赠至青少年体育公益启蒙项目。完赛队伍均可获得公益纪念证书，冠军队获得专业飞盘装备套装。','/images/events/event_20260215121952_ff226d14.jpg','飞盘','school','published','城市体育中心足球场','2026-09-13 06:00:00.000000','2026-09-13 10:00:00.000000','2026-08-19 16:00:00.000000','2026-09-04 16:00:00.000000',0,0,0.00,NULL,NULL,NULL,'赵先生','13766824025',NULL,2,0,'2026-02-03 14:37:24.153705','2026-02-15 04:50:10.276430',1),(13,'「棋逢对手」城市围棋公开赛','面向全市围棋爱好者的智力竞技赛事，按段位分组（业余 1 段及以下、业余 2-4 段、业余 5 段及以上），无报名费，旨在推广围棋文化，提升市民文化素养。\r\n采用中国围棋协会最新竞赛规则，单败淘汰制，每方用时 60 分钟，超时判负；各组别前六名颁发证书及棋具，冠军可代表城市参加省级预选赛。','/images/events/event_20260215145904_fb6cf7b9.jpg','围棋','school','published','市文化艺术中心多功能厅','2026-02-15 07:05:00.000000','2026-02-16 09:00:00.000000','2026-02-15 07:01:00.000000','2026-02-15 07:04:00.000000',0,1,0.00,NULL,NULL,NULL,'郝老师','18709217360',NULL,6,0,'2026-02-15 07:00:57.044601','2026-02-15 07:00:59.485658',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite`
--

LOCK TABLES `favorite` WRITE;
/*!40000 ALTER TABLE `favorite` DISABLE KEYS */;
INSERT INTO `favorite` (`id`, `object_id`, `remarks`, `created_at`, `content_type_id`, `user_id`) VALUES (9,13,NULL,'2026-02-15 07:04:18.497824',7,120);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `like`
--

LOCK TABLES `like` WRITE;
/*!40000 ALTER TABLE `like` DISABLE KEYS */;
INSERT INTO `like` (`id`, `object_id`, `created_at`, `content_type_id`, `user_id`) VALUES (5,13,'2026-02-15 07:04:17.216254',7,120);
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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referee_event_access`
--

LOCK TABLES `referee_event_access` WRITE;
/*!40000 ALTER TABLE `referee_event_access` DISABLE KEYS */;
INSERT INTO `referee_event_access` (`id`, `created_at`, `event_id`, `referee_id`) VALUES (9,'2026-02-02 08:24:16.058026',5,9),(10,'2026-02-03 03:15:11.276275',5,112),(11,'2026-02-03 03:15:14.380821',5,119),(12,'2026-02-15 04:51:45.894140',6,115),(13,'2026-02-15 04:51:45.894162',9,115),(14,'2026-02-15 04:51:45.894173',12,115),(15,'2026-02-15 04:51:49.833093',10,114),(16,'2026-02-15 04:51:49.833114',7,114),(17,'2026-02-15 04:51:49.833125',11,114),(18,'2026-02-15 04:51:53.766850',11,119),(19,'2026-02-15 04:51:53.766890',9,119),(20,'2026-02-15 04:51:59.666772',12,113),(21,'2026-02-15 04:51:59.666792',8,113),(22,'2026-02-15 04:51:59.666803',6,113),(23,'2026-02-15 04:51:59.666812',10,113),(24,'2026-02-15 04:52:06.642157',7,118),(25,'2026-02-15 04:52:06.642199',11,118),(26,'2026-02-15 04:52:06.642225',9,118),(27,'2026-02-15 04:52:06.642250',6,118),(28,'2026-02-15 04:52:10.690325',12,111),(29,'2026-02-15 04:52:10.690367',9,111),(30,'2026-02-15 04:52:10.690394',11,111),(31,'2026-02-15 04:52:10.690420',7,111),(32,'2026-02-15 04:52:20.328813',10,110),(33,'2026-02-15 04:52:20.328835',7,110),(34,'2026-02-15 04:52:20.328846',8,110),(35,'2026-02-15 04:52:20.328855',5,110),(36,'2026-02-15 04:52:20.328865',12,110),(37,'2026-02-15 04:52:25.932316',12,117),(38,'2026-02-15 04:52:25.932339',9,117),(39,'2026-02-15 04:52:25.932349',7,117),(40,'2026-02-15 04:52:25.932361',5,117),(41,'2026-02-15 04:52:25.932370',10,117),(42,'2026-02-15 04:52:31.383606',12,116),(43,'2026-02-15 04:52:31.383626',9,116),(44,'2026-02-15 04:52:31.383637',7,116),(45,'2026-02-15 04:52:31.383647',11,116),(46,'2026-02-15 04:52:38.007157',12,9),(47,'2026-02-15 04:52:38.007196',11,9),(48,'2026-02-15 04:52:38.007223',10,9),(49,'2026-02-15 04:52:38.007248',9,9),(50,'2026-02-15 04:52:38.007272',8,9),(51,'2026-02-15 04:52:38.007298',7,9),(52,'2026-02-15 04:52:38.007322',6,9),(53,'2026-02-15 07:04:52.986068',13,112),(54,'2026-02-15 07:06:11.629532',13,9);
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
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` (`id`, `status`, `registration_number`, `participant_name`, `participant_phone`, `participant_id_card`, `participant_gender`, `participant_birth_date`, `participant_organization`, `emergency_contact`, `emergency_phone`, `payment_status`, `payment_amount`, `payment_time`, `remarks`, `review_remarks`, `reviewed_at`, `created_at`, `updated_at`, `event_id`, `reviewed_by_id`, `user_id`) VALUES (2,'approved','REG-5-20260201082151-2B61151A','张三','13725629630','51323219961104755X','M','1996-11-04','','张先生','15271972431','unpaid',0.00,NULL,'','','2026-02-01 08:23:55.967640','2026-02-01 08:21:51.654466','2026-02-01 08:23:55.967813',5,1,6),(3,'approved','REG-5-20260201082233-4326653B','李四','13913737767','50011419970105323X','M','1997-01-05','','李先生','13766921774','unpaid',0.00,NULL,'','','2026-02-01 08:23:57.404392','2026-02-01 08:22:33.323362','2026-02-01 08:23:57.404560',5,1,7),(4,'approved','REG-5-20260201082339-610DC4F5','王五','15298052283','650421199905310544','M','1999-05-31','城市实验中学','王先生','15246009563','unpaid',0.00,NULL,'','','2026-02-01 08:23:58.473829','2026-02-01 08:23:39.698131','2026-02-01 08:23:58.473994',5,1,8),(102,'approved','REG-5-20260203153041-F6B0D91B','张一诺','15034567890','110105199501016267','M','1995-01-01',NULL,'黄奕辰','13841843776','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.276189','2026-02-03 07:30:41.276203',5,1,12),(103,'approved','REG-5-20260203153041-06B3C91F','上官梓轩','18867890123','110105199501012901','M','1995-01-01',NULL,'吴泽宇','13616543544','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.286221','2026-02-03 07:30:41.286228',5,1,15),(104,'approved','REG-5-20260203153041-500419F9','诸葛俊豪','13690123456','110105199501018086','M','1995-01-01',NULL,'陈俊豪','18216184322','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.294922','2026-02-03 07:30:41.294931',5,1,18),(105,'approved','REG-5-20260203153041-F23AC0EB','闻人欣怡','15123456789','110105199501013672','M','1995-01-01',NULL,'袁一诺','13458097812','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.302306','2026-02-03 07:30:41.302314',5,1,21),(106,'approved','REG-5-20260203153041-D708AAE5','马丽','17745678901','110105199501016160','M','1995-01-01',NULL,'田泽宇','18447643218','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.309718','2026-02-03 07:30:41.309726',5,1,23),(107,'approved','REG-5-20260203153041-DA2FCB7C','刘芳','13578901234','110105199501014480','M','1995-01-01',NULL,'程俊峰','13682221972','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.317320','2026-02-03 07:30:41.317328',5,1,26),(108,'approved','REG-5-20260203153041-32DD37F0','郭悦','15701234567','110105199501011212','M','1995-01-01',NULL,'赵浩然','13510240000','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.325578','2026-02-03 07:30:41.325586',5,1,29),(109,'approved','REG-5-20260203153041-B296EDF9','欧阳浩然','17612345678','110105199501014771','M','1995-01-01',NULL,'余欣悦','15963094352','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.333262','2026-02-03 07:30:41.333270',5,1,30),(110,'approved','REG-5-20260203153041-CDFCF31D','林涛','13345678901','110105199501011159','M','1995-01-01',NULL,'于静怡','19811565152','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.341913','2026-02-03 07:30:41.341921',5,1,33),(111,'approved','REG-5-20260203153041-BD181FB9','罗欣怡','15367890123','110105199501013728','M','1995-01-01',NULL,'刘语桐','13625693917','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:24.172167','2026-02-03 07:30:41.349549','2026-02-03 07:30:41.349557',5,1,35),(112,'approved','REG-5-20260203153041-1C69546B','司徒思琪','17589012345','110105199501015547','M','1995-01-01',NULL,'韩雨桐','18856115745','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.357340','2026-02-03 07:30:41.357348',5,1,37),(113,'approved','REG-5-20260203153041-EEDF4710','唐静','19601234567','11010519950101646X','M','1995-01-01',NULL,'叶博文','18499097379','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.366232','2026-02-03 07:30:41.366242',5,1,39),(114,'approved','REG-5-20260203153041-123F004F','韩泽宇','13023456789','110105199501013779','M','1995-01-01',NULL,'傅雨欣','15841624919','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.374332','2026-02-03 07:30:41.374341',5,1,41),(115,'approved','REG-5-20260203153041-62784CD5','曹佳','14934567890','110105199501016590','M','1995-01-01',NULL,'雷俊豪','15124037308','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.382578','2026-02-03 07:30:41.382587',5,1,42),(116,'approved','REG-5-20260203153041-6F1CA68D','邓浩然','17156789012','110105199501015571','M','1995-01-01',NULL,'蔡宇轩','18739089796','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.391169','2026-02-03 07:30:41.391178',5,1,44),(117,'approved','REG-5-20260203153041-BB139EA9','诸葛瑞','18978901234','110105199501010279','M','1995-01-01',NULL,'潘凯','13667431335','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.398967','2026-02-03 07:30:41.398974',5,1,46),(118,'approved','REG-5-20260203153041-C4D36A2A','肖强','19290123456','110105199501012055','M','1995-01-01',NULL,'曾奕辰','15228570723','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.406416','2026-02-03 07:30:41.406423',5,1,48),(119,'approved','REG-5-20260203153041-1C530ECA','田思琪','13912345678','110105199501018617','M','1995-01-01',NULL,'周玥','13856396276','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.414244','2026-02-03 07:30:41.414253',5,1,50),(120,'approved','REG-5-20260203153041-BE8FDDCC','赫连峰','15934567890','110105199501016275','M','1995-01-01',NULL,'彭语桐','15045638569','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.422286','2026-02-03 07:30:41.422294',5,1,52),(121,'approved','REG-5-20260203153041-49180AD1','袁一诺','17845678901','110105199501015942','M','1995-01-01',NULL,'唐宇辰','15011497120','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:21.497880','2026-02-03 07:30:41.430413','2026-02-03 07:30:41.430421',5,1,53),(122,'approved','REG-5-20260203153041-40AB1747','澹台欣','19967890123','11010519950101291X','M','1995-01-01',NULL,'董思琪','15747365070','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.438464','2026-02-03 07:30:41.438473',5,1,55),(123,'approved','REG-5-20260203153041-BA8B1F20','蒋静','13689012345','110105199501010033','M','1995-01-01',NULL,'苏雨桐','19890231003','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.446314','2026-02-03 07:30:41.446324',5,1,57),(124,'approved','REG-5-20260203153041-66074D0C','蔡浩然','14501234567','110105200103149641','M','2001-03-14',NULL,'杜梓琪','13511460562','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.461970','2026-02-03 07:30:41.462029',5,1,59),(125,'approved','REG-5-20260203153041-A1AF9D81','上官琪','15823456789','110105199501012493','M','1995-01-01',NULL,'徐思琪','15818915545','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.470323','2026-02-03 07:30:41.470331',5,1,61),(126,'approved','REG-5-20260203153041-8055444A','杜泽宇','17734567890','110105199501015387','M','1995-01-01',NULL,'方沐宸','18257778008','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.478718','2026-02-03 07:30:41.478726',5,1,62),(127,'approved','REG-5-20260203153041-C9015608','皇甫明','19856789012','110105199501011108','M','1995-01-01',NULL,'高梓琪','18247839193','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.487479','2026-02-03 07:30:41.487487',5,1,64),(128,'approved','REG-5-20260203153041-EF09BD51','吕悦','13478901234','11010519950101267X','M','1995-01-01',NULL,'魏沐阳','13536373598','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.496460','2026-02-03 07:30:41.496468',5,1,66),(129,'approved','REG-5-20260203153041-3771BF3C','魏一诺','15790123456','110105199501017876','M','1995-01-01',NULL,'蒋晓雅','15066728979','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.507496','2026-02-03 07:30:41.507507',5,1,68),(130,'approved','REG-5-20260203153041-31959CF9','长孙佳','18612345678','110105199501013234','M','1995-01-01',NULL,'江雨桐','13617396443','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.516972','2026-02-03 07:30:41.516984',5,1,70),(131,'approved','REG-5-20260203153041-76808696','陆静','13334567890','110105199501018465','M','1995-01-01',NULL,'肖玥','18329629390','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:19.659561','2026-02-03 07:30:41.525773','2026-02-03 07:30:41.525783',5,1,72),(132,'approved','REG-5-20260203153041-FE9D49F4','夏浩然','15356789012','110105199501011685','M','1995-01-01',NULL,'温宇辰','18730384987','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.534781','2026-02-03 07:30:41.534792',5,1,74),(133,'approved','REG-5-20260203153041-C5771DCB','钟芳','15667890123','110105199501016996','M','1995-01-01',NULL,'梁沐阳','18760227493','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.543931','2026-02-03 07:30:41.543943',5,1,75),(134,'approved','REG-5-20260203153041-0DAF6D75','汪泽宇','18589012345','110105199501012231','M','1995-01-01',NULL,'白思彤','13449321771','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.554261','2026-02-03 07:30:41.554275',5,1,77),(135,'approved','REG-5-20260203153041-2E7636CA','欧阳雪','13101234567','11010519950101574X','M','1995-01-01',NULL,'何欣悦','13908429128','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.562736','2026-02-03 07:30:41.562746',5,1,79),(136,'approved','REG-5-20260203153041-94E20093','董思琪','13012345678','110105199501018211','M','1995-01-01',NULL,'邓沐宸','13965425487','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.572307','2026-02-03 07:30:41.572319',5,1,80),(137,'approved','REG-5-20260203153041-1F29F4C2','澹台泽宇','17034567890','110105199501016910','M','1995-01-01',NULL,'朱静怡','13502375782','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.581420','2026-02-03 07:30:41.581436',5,1,82),(138,'approved','REG-5-20260203153041-7CE28537','于强','18056789012','110105199501014931','M','1995-01-01',NULL,'罗俊峰','17854544241','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.591390','2026-02-03 07:30:41.591402',5,1,84),(139,'approved','REG-5-20260203153041-7758ACD2','蔡静','19178901234','110105199706017642','M','1997-06-01',NULL,'郑雨欣','13762884879','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.609727','2026-02-03 07:30:41.609740',5,1,86),(140,'approved','REG-5-20260203153041-5A0C97E2','慕容琪','13890123456','110105199501013787','M','1995-01-01',NULL,'王梓涵','13775221697','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.640455','2026-02-03 07:30:41.640463',5,1,88),(141,'approved','REG-5-20260203153041-91BB747F','苏思琪','13901234567','110105199501011757','M','1995-01-01',NULL,'胡博文','17882014648','unpaid',0.00,NULL,NULL,'','2026-02-03 07:31:23.608794','2026-02-03 07:30:41.662703','2026-02-03 07:30:41.662714',5,1,89),(142,'approved','REG-5-20260203153041-0EE5819F','叶泽宇','15923456789','110105199501019556','M','1995-01-01',NULL,'孙一诺','18893544957','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.681291','2026-02-03 07:30:41.681299',5,1,91),(143,'approved','REG-5-20260203153041-C547A900','吕一诺','18845678901','110105199501018393','M','1995-01-01',NULL,'薛一诺','18265884111','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.696207','2026-02-03 07:30:41.696222',5,1,93),(144,'approved','REG-5-20260203153041-E3C4CC40','薛梓轩','13767890123','110105199501017067','M','1995-01-01',NULL,'马凯','15190960156','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.705041','2026-02-03 07:30:41.705048',5,1,95),(145,'approved','REG-5-20260203153041-022D2431','金静','13678901234','110105199501013293','M','1995-01-01',NULL,'宋思彤','18429705685','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.725136','2026-02-03 07:30:41.725150',5,1,96),(146,'approved','REG-5-20260203153041-EE1AC88B','司马杰','14789012345','110105199501011335','M','1995-01-01',NULL,'李沐宸','15774244354','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.736647','2026-02-03 07:30:41.736655',5,1,97),(147,'approved','REG-5-20260203153041-9929AC20','陆思琪','14590123456','110105199501013963','M','1995-01-01',NULL,'郭宇轩','13731259853','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.745077','2026-02-03 07:30:41.745090',5,1,98),(148,'approved','REG-5-20260203153041-C2953C87','尉迟浩然','15812345678','110105199501015539','M','1995-01-01',NULL,'曹俊豪','13748975077','unpaid',0.00,NULL,NULL,'','2026-02-03 07:36:10.660827','2026-02-03 07:30:41.754022','2026-02-03 07:30:41.754035',5,1,100),(149,'approved','REG-5-20260203153041-E281DA00','慕容泽宇','15945678901','110105199806226820','M','1998-06-22',NULL,'谢一诺','18809302418','unpaid',0.00,NULL,NULL,'','2026-02-03 07:33:26.797188','2026-02-03 07:30:41.769876','2026-02-03 07:33:26.797366',5,1,13),(150,'approved','REG-5-20260203153041-8C058D54','周诗雨','14701234567','110105199501016419','M','1995-01-01',NULL,'石语桐','18871889902','unpaid',0.00,NULL,NULL,'','2026-02-03 07:33:25.448092','2026-02-03 07:30:41.778039','2026-02-03 07:33:25.448194',5,1,19),(151,'approved','REG-5-20260203153041-7F406EA9','澹台一诺','13489012345','110105199501014667','M','1995-01-01',NULL,'林晓雅','15274496015','unpaid',0.00,NULL,NULL,'','2026-02-03 07:33:23.837274','2026-02-03 07:30:41.786882','2026-02-03 07:33:23.837368',5,1,27),(153,'approved','REG-13-20260215070356-63C76863','王生生','13287963401','310101200010100928','M','2000-10-10','','王先生','18019283672','unpaid',0.00,NULL,'','','2026-02-15 07:04:03.474623','2026-02-15 07:03:56.154375','2026-02-15 07:04:03.474715',13,1,120);
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
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` (`id`, `round_type`, `score`, `rank`, `award`, `score_unit`, `remarks`, `certificate_url`, `is_published`, `created_at`, `updated_at`, `event_id`, `recorded_by_id`, `registration_id`, `user_id`) VALUES (109,'final','02:06:26',1,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.612150','2026-02-03 07:36:33.612161',5,1,4,8),(110,'final','02:06:47',2,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.618895','2026-02-03 07:36:33.618906',5,1,2,6),(111,'final','02:07:00',3,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.626083','2026-02-03 07:36:33.626094',5,1,3,7),(112,'final','02:09:15',4,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.632395','2026-02-03 07:36:33.632407',5,1,151,27),(113,'final','02:17:42',5,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.638698','2026-02-03 07:36:33.638709',5,1,150,19),(114,'final','02:28:36',6,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.644985','2026-02-03 07:36:33.644997',5,1,149,13),(115,'final','02:35:09',7,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.651259','2026-02-03 07:36:33.651271',5,1,148,100),(116,'final','02:41:57',8,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.657442','2026-02-03 07:36:33.657452',5,1,147,98),(117,'final','02:53:21',9,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.664218','2026-02-03 07:36:33.664230',5,1,146,97),(118,'final','03:01:05',10,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.670797','2026-02-03 07:36:33.670809',5,1,145,96),(119,'final','03:08:33',11,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.677872','2026-02-03 07:36:33.677884',5,1,144,95),(120,'final','03:15:27',12,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.684600','2026-02-03 07:36:33.684612',5,1,143,93),(121,'final','03:22:49',13,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.692027','2026-02-03 07:36:33.692040',5,1,142,91),(122,'final','03:29:18',14,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.698494','2026-02-03 07:36:33.698505',5,1,141,89),(123,'final','03:37:51',15,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.705077','2026-02-03 07:36:33.705090',5,1,140,88),(124,'final','03:44:06',16,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.711660','2026-02-03 07:36:33.711672',5,1,139,86),(125,'final','03:52:39',17,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.718090','2026-02-03 07:36:33.718101',5,1,138,84),(126,'final','03:58:14',18,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.724636','2026-02-03 07:36:33.724647',5,1,137,82),(127,'final','04:03:28',19,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.731116','2026-02-03 07:36:33.731127',5,1,136,80),(128,'final','04:09:55',20,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.738082','2026-02-03 07:36:33.738095',5,1,135,79),(129,'final','04:16:12',21,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.745265','2026-02-03 07:36:33.745277',5,1,134,77),(130,'final','04:23:47',22,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.751976','2026-02-03 07:36:33.751988',5,1,133,75),(131,'final','04:28:03',23,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.759068','2026-02-03 07:36:33.759080',5,1,132,74),(132,'final','02:11:29',24,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.765947','2026-02-03 07:36:33.765959',5,1,131,72),(133,'final','02:19:53',25,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.775510','2026-02-03 07:36:33.775522',5,1,130,70),(134,'final','02:31:45',26,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.784395','2026-02-03 07:36:33.784409',5,1,129,68),(135,'final','02:47:02',27,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.791082','2026-02-03 07:36:33.791094',5,1,128,66),(136,'final','02:58:38',28,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.797813','2026-02-03 07:36:33.797824',5,1,127,64),(137,'final','03:05:17',29,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.804574','2026-02-03 07:36:33.804586',5,1,126,62),(138,'final','03:12:41',30,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.811124','2026-02-03 07:36:33.811137',5,1,125,61),(139,'final','03:19:08',31,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.817946','2026-02-03 07:36:33.817959',5,1,124,59),(140,'final','03:26:32',32,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.824763','2026-02-03 07:36:33.824776',5,1,123,57),(141,'final','03:33:58',33,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.831497','2026-02-03 07:36:33.831508',5,1,122,55),(142,'final','03:41:24',34,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.838177','2026-02-03 07:36:33.838188',5,1,121,53),(143,'final','03:48:01',35,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.844817','2026-02-03 07:36:33.844828',5,1,120,52),(144,'final','03:55:36',36,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.851744','2026-02-03 07:36:33.851756',5,1,119,50),(145,'final','04:06:42',37,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.858497','2026-02-03 07:36:33.858508',5,1,118,48),(146,'final','04:13:19',38,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.864955','2026-02-03 07:36:33.864966',5,1,117,46),(147,'final','04:19:56',39,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.871479','2026-02-03 07:36:33.871489',5,1,116,44),(148,'final','04:25:22',40,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.878024','2026-02-03 07:36:33.878034',5,1,115,42),(149,'final','04:31:09',41,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.885005','2026-02-03 07:36:33.885017',5,1,114,41),(150,'final','04:38:45',42,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.891554','2026-02-03 07:36:33.891565',5,1,113,39),(151,'final','04:45:13',43,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.897783','2026-02-03 07:36:33.897794',5,1,112,37),(152,'final','04:51:37',44,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.904540','2026-02-03 07:36:33.904555',5,1,111,35),(153,'final','04:57:22',45,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.911045','2026-02-03 07:36:33.911057',5,1,110,33),(154,'final','05:00:00',46,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.920927','2026-02-03 07:36:33.920939',5,1,109,30),(155,'final','02:13:46',47,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.928463','2026-02-03 07:36:33.928474',5,1,108,29),(156,'final','02:25:11',48,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.936489','2026-02-03 07:36:33.936501',5,1,107,26),(157,'final','02:38:04',49,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.944327','2026-02-03 07:36:33.944339',5,1,106,23),(158,'final','02:49:35',50,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.952419','2026-02-03 07:36:33.952431',5,1,105,21),(159,'final','03:03:59',51,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.960504','2026-02-03 07:36:33.960515',5,1,104,18),(160,'final','03:10:26',52,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.968468','2026-02-03 07:36:33.968479',5,1,103,15),(161,'final','04:49:08',53,NULL,NULL,NULL,NULL,1,'2026-02-03 07:36:33.976069','2026-02-03 07:36:33.976080',5,1,102,12),(163,'final','1',1,NULL,NULL,NULL,NULL,1,'2026-02-15 07:19:58.818298','2026-02-15 07:20:43.168280',13,9,153,120);
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
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `real_name`, `phone`, `user_type`, `avatar`, `gender`, `birth_date`, `id_card`, `emergency_contact`, `emergency_phone`, `organization`, `bio`, `is_verified`, `created_at`, `updated_at`) VALUES (1,'pbkdf2_sha256$720000$Wa1bxOhfJbm9zqzCnIGten$lE7cGDTnb2oVLhFd2P5bdbML9KFXrndVFyYE8+CNKx4=','2026-02-15 06:58:03.431779',1,'admin','','','admin@sports.cn',1,1,'2025-10-31 21:42:19.753186','管理员','16628770995','admin','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-10-31 21:42:19.753186','2026-02-03 03:02:49.661741'),(6,'pbkdf2_sha256$720000$rYzpMTOk7LdxEOUzIYQurD$v7P5bnYmejJ+9M8OE1hk3oNRHEjO9ha+OhZqEzBU0wY=','2026-02-03 07:43:10.278128',0,'张三','','','zhangsan@sports.cn',0,1,'2025-11-02 01:28:45.619872','张三','13725629630','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-02 01:28:45.619872','2026-02-03 03:02:49.662609'),(7,'pbkdf2_sha256$720000$UV1wPUvrXAwsNRF0ysaF8K$ku+AYt8aC7vx5g3aAhGKrK9XFKjXekZm0hAgAu4Kly0=','2026-02-03 07:45:26.650747',0,'李四','','','lisi@sports.cn',0,1,'2025-11-03 06:59:22.876459','李四','13913737767','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-03 06:59:22.876459','2026-02-03 03:02:49.663337'),(8,'pbkdf2_sha256$720000$Ds1AMrjPRJkaKgmF8MRiJ4$p+weEgnuK/xOUA5GK4+RlTQgVvD+HrTjU82WjCMpESc=','2026-02-02 14:53:22.906615',0,'王五','','','wangwu@sports.cn',0,1,'2025-11-04 10:11:58.342915','王五','15298052283','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-04 10:11:58.342915','2026-02-03 03:02:49.663966'),(9,'pbkdf2_sha256$720000$cDnmoOoZpkdaFME5wLXD1F$OAT6mzn3ApNCfhZd910akqS+f07GgNJBSxL9I2Fn+Uw=','2026-02-15 07:06:23.722089',0,'李寻欢','','','lixunhuan@sports.cn',1,1,'2025-11-05 16:05:33.698572','李寻欢','15210123318','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-05 16:05:33.698572','2026-02-03 03:02:49.664525'),(10,'pbkdf2_sha256$720000$qUsC9hNJQnFvfo0BK5TLxK$9eMQxbmmiyvmg5yMac8KpkKBWRcq5DGYirDjtht8PtE=',NULL,0,'皇甫雨桐','','','huangfuyutong@sports.cn',0,1,'2025-11-05 20:22:47.185239','皇甫雨桐','13898765432','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-05 20:22:47.185239','2026-02-03 03:02:49.665051'),(11,'pbkdf2_sha256$720000$rfaS9cMTdyA0mP3LJmRnKB$ys9RLP2FwCjSX497eKBaeqCzcpG5Niy1/IYvK9BKpKw=',NULL,0,'陈阳','','','chenyang@sports.cn',0,1,'2025-11-07 00:59:15.741896','陈阳','13923456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-07 00:59:15.741896','2026-02-03 03:02:49.665523'),(12,'pbkdf2_sha256$720000$9B238dq5YGJ7wMJVEBVyUo$bAKSJpmc1H0QHL0hcbzih3ugmOfemLrE7UiMJz2KFgA=',NULL,0,'张一诺','','','zhangyinuo@sports.cn',0,1,'2025-11-08 05:16:09.258451','张一诺','15034567890','athlete','',NULL,'1995-01-01','110105199501016267',NULL,NULL,NULL,NULL,0,'2025-11-08 05:16:09.258451','2026-02-03 03:02:49.665981'),(13,'pbkdf2_sha256$720000$DXJPeZYSa698uqn7EUzhRL$dSQPirf4buGTwIKRi/Lo4Na15A9/KY1CazRozApagKE=','2026-02-03 07:46:40.550014',0,'慕容泽宇','','','murongzeyu@sports.cn',0,1,'2025-11-09 09:44:32.895178','慕容泽宇','15945678901','athlete','',NULL,'1998-06-22','110105199806226820',NULL,NULL,NULL,NULL,0,'2025-11-09 09:44:32.895178','2026-02-03 03:02:49.666438'),(14,'pbkdf2_sha256$720000$gThXdHexbEgqanHA6sFCIZ$+fcCZn/fq1Ta+4GVlzUmPEuORIC2lekxwKqrRCsxrlo=',NULL,0,'赵静','','','zhaojing@sports.cn',0,1,'2025-11-10 17:28:05.369745','赵静','17856789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-10 17:28:05.369745','2026-02-03 03:02:49.666883'),(15,'pbkdf2_sha256$720000$X3mM6vsqp7pvikB7xybPnX$47j3e7DKTjrkNOJO6LfM6yM4+ls99ka5AGbDwqPqTEU=',NULL,0,'上官梓轩','','','shangguanxuan@sports.cn',0,1,'2025-11-10 22:59:22.816391','上官梓轩','18867890123','athlete','',NULL,'1995-01-01','110105199501012901',NULL,NULL,NULL,NULL,0,'2025-11-10 22:59:22.816391','2026-02-03 03:02:49.667394'),(16,'pbkdf2_sha256$720000$ViCw4gvX7pxGVnUysaaIJK$uhBpqiIUp3yyA2LVd+RN/MuiKjhm97zrM/NgbB+p08U=',NULL,0,'李浩然','','','lihaoran@sports.cn',0,1,'2025-11-12 02:33:47.652857','李浩然','19978901234','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-12 02:33:47.652857','2026-02-03 03:02:49.667865'),(17,'pbkdf2_sha256$720000$dkiYrYyRMXBA6gcTISClYN$zfgbe4PfAb5z+vDNJsKReVzhPoMrZc1r/dt6TzEFpzI=',NULL,0,'孙强','','','sunqiang@sports.cn',0,1,'2025-11-13 07:15:22.198426','孙强','13789012345','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-13 07:15:22.198426','2026-02-03 03:02:49.668319'),(18,'pbkdf2_sha256$720000$rNHJcxyHHzrk9DBMsSwieu$nAtW76I2Vaf5l4GMcHS2CJefVp9oxTEy0ChkZlOjwpU=',NULL,0,'诸葛俊豪','','','zhuguijunhao@sports.cn',0,1,'2025-11-14 11:48:59.765893','诸葛俊豪','13690123456','athlete','',NULL,'1995-01-01','110105199501018086',NULL,NULL,NULL,NULL,0,'2025-11-14 11:48:59.765893','2026-02-03 03:02:49.668716'),(19,'pbkdf2_sha256$720000$dwjCYpHTAjYh4lGG06PVWD$wckI+S0Scx4HJa7qPm6IzaB5xlz4SsMhCPcTn57W4Io=','2026-02-03 07:46:23.939097',0,'周诗雨','','','zhoushiyu@sports.cn',0,1,'2025-11-15 18:15:11.239458','周诗雨','14701234567','athlete','',NULL,'1995-01-01','110105199501016419',NULL,NULL,NULL,NULL,0,'2025-11-15 18:15:11.239458','2026-02-03 03:02:49.669160'),(20,'pbkdf2_sha256$720000$hV7dNQ01pjntmLzPdl0pWA$4EYSYvoDBeVaCYphjog1zWz5PA7cQRrYX32t+qsB73k=',NULL,0,'吴涛','','','wutao@sports.cn',0,1,'2025-11-15 21:33:44.785192','吴涛','14512345678','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-15 21:33:44.785192','2026-02-03 03:02:49.669706'),(21,'pbkdf2_sha256$720000$NFabpjKghyJ7VttTHxsdWo$MJhRb+UGFz/1brhh8B9FOdHIEdffN1SABa0NfsnAtGk=',NULL,0,'闻人欣怡','','','wenrenxinyi@sports.cn',0,1,'2025-11-17 01:42:09.652876','闻人欣怡','15123456789','athlete','',NULL,'1995-01-01','110105199501013672',NULL,NULL,NULL,NULL,0,'2025-11-17 01:42:09.652876','2026-02-03 03:02:49.670209'),(22,'pbkdf2_sha256$720000$uAOxF5lvwkg2AAhhEp559F$+0S6ohhnePaYgeU8UhxYkBKbeDHLtJYNan0jCS51NsY=',NULL,0,'郑泽宇','','','zhengzeyu@sports.cn',0,1,'2025-11-18 06:26:33.189452','郑泽宇','15834567890','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-18 06:26:33.189452','2026-02-03 03:02:49.670656'),(23,'pbkdf2_sha256$720000$uLunv12HBcEIjgFEiRhvDI$xvgrBjO7sOSAHFa3XATk3ZDiXi/Ie9hNy+fPLWWI0VE=',NULL,0,'马丽','','','mali@sports.cn',0,1,'2025-11-19 10:59:09.756189','马丽','17745678901','athlete','',NULL,'1995-01-01','110105199501016160',NULL,NULL,NULL,NULL,0,'2025-11-19 10:59:09.756189','2026-02-03 03:02:49.671104'),(24,'pbkdf2_sha256$720000$3Grw3NHMdxaFCoPadY8nLY$RSqp73GENutsiX4P2siWJF0cFv9dJ2L9AvZLhnNPuiA=',NULL,0,'赫连子昂','','','helianziang@sports.cn',0,1,'2025-11-20 16:22:33.249756','赫连子昂','18756789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-20 16:22:33.249756','2026-02-03 03:02:49.671684'),(25,'pbkdf2_sha256$720000$B4oE7EetCOMXW8dCiCURmT$wTYwUfXl43uw2Dz0v5Zb4fTI514gp35+W8hETK6LEOI=',NULL,0,'王梓琪','','','wangziqi@sports.cn',0,1,'2025-11-20 20:56:09.785423','王梓琪','19867890123','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-20 20:56:09.785423','2026-02-03 03:02:49.672307'),(26,'pbkdf2_sha256$720000$hJVRC2U5ldNcNK4nNGIQWf$y3pxXkDAQIDJndb8XLzX/7RaxLFrIeMlcpuVRR9M1G8=',NULL,0,'刘芳','','','liufang@sports.cn',0,1,'2025-11-22 00:45:22.369189','刘芳','13578901234','athlete','',NULL,'1995-01-01','110105199501014480',NULL,NULL,NULL,NULL,0,'2025-11-22 00:45:22.369189','2026-02-03 03:02:49.672899'),(27,'pbkdf2_sha256$720000$zntBpWiXi5MuQAcksHZHQz$hoTKNNCyy8HF94Sxc8BCiOh55qqdKKEPZK9ftxlx0jE=','2026-02-03 07:45:53.798798',0,'澹台一诺','','','tantayinuo@sports.cn',0,1,'2025-11-23 05:19:09.856745','澹台一诺','13489012345','athlete','',NULL,'1995-01-01','110105199501014667',NULL,NULL,NULL,NULL,0,'2025-11-23 05:19:09.856745','2026-02-03 03:02:49.673359'),(28,'pbkdf2_sha256$720000$a1zyI00CJmHUyFXBrTU72W$pv1IlmDZtU7Ly2iNTNB8umwwxi9qJ+/dDJXCn01KKbg=',NULL,0,'黄俊豪','','','huangjunhao@sports.cn',0,1,'2025-11-24 09:54:33.698421','黄俊豪','15290123456','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-24 09:54:33.698421','2026-02-03 03:02:49.673815'),(29,'pbkdf2_sha256$720000$5ZDZgVZw6NT2BEeVi0pV64$Jc6jomkkdB5ZP6t4hJnS8b/T/VM5gT9tFl4RennahKE=',NULL,0,'郭悦','','','guoyue@sports.cn',0,1,'2025-11-25 17:28:09.156789','郭悦','15701234567','athlete','',NULL,'1995-01-01','110105199501011212',NULL,NULL,NULL,NULL,0,'2025-11-25 17:28:09.156789','2026-02-03 03:02:49.674352'),(30,'pbkdf2_sha256$720000$YkR1poycpXE2CoHliXSaPk$EA47lNdrNJBU+ULLxabl4WA0KMri0uE/ftzlxvT727k=',NULL,0,'欧阳浩然','','','ouyanghaoran@sports.cn',0,1,'2025-11-25 22:35:44.789456','欧阳浩然','17612345678','athlete','',NULL,'1995-01-01','110105199501014771',NULL,NULL,NULL,NULL,0,'2025-11-25 22:35:44.789456','2026-02-03 03:02:49.674840'),(31,'pbkdf2_sha256$720000$WtFih27mItBKZkM5WMNwMv$XRtIxqJmWfoDLoOsIlMTIKVTIRhDSYFIxw2WUOoXYhU=',NULL,0,'何敏','','','hemin@sports.cn',0,1,'2025-11-27 01:59:09.265183','何敏','18623456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-27 01:59:09.265183','2026-02-03 03:02:49.675343'),(32,'pbkdf2_sha256$720000$ypMjT0wFjYqqknpDMmh3jh$uaxA78RmJ1FvNNwMDCkPkW8SN/9psF3tA77hLEeUJyE=',NULL,0,'高思琪','','','gaosiqi@sports.cn',0,1,'2025-11-28 06:42:33.789451','高思琪','19734567890','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-28 06:42:33.789451','2026-02-03 03:02:49.675980'),(33,'pbkdf2_sha256$720000$u0XLxhulH2936fieAlXJcJ$utSRnaxtopfcLr1keB5TON7ITMHJQwXrgXC8W/+CR7E=',NULL,0,'林涛','','','lintao@sports.cn',0,1,'2025-11-29 11:25:22.365189','林涛','13345678901','athlete','',NULL,'1995-01-01','110105199501011159',NULL,NULL,NULL,NULL,0,'2025-11-29 11:25:22.365189','2026-02-03 03:02:49.676568'),(34,'pbkdf2_sha256$720000$34NaT0U0p9VX0KnOjsQoLG$GyiqbLbkl7dmxr4ori8DFK8Ky5nTW7JqjOdLwri1/QI=',NULL,0,'司马诗雨','','','simashiyu@sports.cn',0,1,'2025-11-30 16:59:09.789456','司马诗雨','13256789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-30 16:59:09.789456','2026-02-03 03:02:49.677074'),(35,'pbkdf2_sha256$720000$Nx5xBniO2MErX6EC1zUpDt$GQKQdWDTZRwpQKq0lSy2gJFIreNVxV/1vqjiPeSFt3Y=',NULL,0,'罗欣怡','','','luoxinyi@sports.cn',0,1,'2025-11-30 21:36:44.652189','罗欣怡','15367890123','athlete','',NULL,'1995-01-01','110105199501013728',NULL,NULL,NULL,NULL,0,'2025-11-30 21:36:44.652189','2026-02-03 03:02:49.677530'),(36,'pbkdf2_sha256$720000$AE14PNodoUgXQgetiChCCu$NWpZfyEqGElKbi9x0FDUZpdUyoxD0ueIXDuV8dQcHjs=',NULL,0,'宋阳','','','songyang@sports.cn',0,1,'2025-12-02 01:55:22.189456','宋阳','15678901234','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-02 01:55:22.189456','2026-02-03 03:02:49.678092'),(37,'pbkdf2_sha256$720000$CmTpng1a144dozYR90gE7l$5jh09yTriRLi2hYeW4QcS9eVliQbuTgqDcYGAN3ZOPw=',NULL,0,'司徒思琪','','','situsiqi@sports.cn',0,1,'2025-12-03 06:42:09.652893','司徒思琪','17589012345','athlete','',NULL,'1995-01-01','110105199501015547',NULL,NULL,NULL,NULL,0,'2025-12-03 06:42:09.652893','2026-02-03 03:02:49.678591'),(38,'pbkdf2_sha256$720000$zBnANfn8Tw3bNfp8V8ssfM$fnJ+80Nb+U+mEllU4ehYl5Ykvg56DuHSV1ThElAKwpk=',NULL,0,'谢子昂','','','xieziang@sports.cn',0,1,'2025-12-04 10:36:33.249561','谢子昂','18590123456','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-04 10:36:33.249561','2026-02-03 03:02:49.679071'),(39,'pbkdf2_sha256$720000$fQwdGPS8M0AVhidBanDYqS$Id+JXlA8MbQag7QOf3Qo3R/AovZYHbENYtRUVmt4cxg=',NULL,0,'唐静','','','tangjing@sports.cn',0,1,'2025-12-05 16:19:09.785428','唐静','19601234567','athlete','',NULL,'1995-01-01','11010519950101646X',NULL,NULL,NULL,NULL,0,'2025-12-05 16:19:09.785428','2026-02-03 03:02:49.679519'),(40,'pbkdf2_sha256$720000$ozKtpivJQ5v8NR9vRBpWr0$c+BGi3l6dPETuKqpDVLWgYHye2d3kCdaNxH9WwoV7Tc=',NULL,0,'长孙悦','','','zhangsunyue@sports.cn',0,1,'2025-12-05 20:55:44.265189','长孙悦','13112345678','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-05 20:55:44.265189','2026-02-03 03:02:49.680083'),(41,'pbkdf2_sha256$720000$7g0TL2nkilaNvgKPMK9JB5$+uduwai5c9dnP5Lyh8TjUsgpMOfvuMMQF/IMiqSiH98=',NULL,0,'韩泽宇','','','hanzeyu@sports.cn',0,1,'2025-12-07 00:32:09.789456','韩泽宇','13023456789','athlete','',NULL,'1995-01-01','110105199501013779',NULL,NULL,NULL,NULL,0,'2025-12-07 00:32:09.789456','2026-02-03 03:02:49.680577'),(42,'pbkdf2_sha256$720000$8NTCg7ltvA4VUH15F16wHQ$cFg10vp/wUIYStWS5sOj4bxOdv36eCP+I0iR57vkxsU=',NULL,0,'曹佳','','','caojia@sports.cn',0,1,'2025-12-08 05:16:33.652189','曹佳','14934567890','athlete','',NULL,'1995-01-01','110105199501016590',NULL,NULL,NULL,NULL,0,'2025-12-08 05:16:33.652189','2026-02-03 03:02:49.681008'),(43,'pbkdf2_sha256$720000$xZQo5a1eBQYktkPuvOOD1j$4FZ2+2mNLfWw+eBdOT4qfiVYioL+yj5GlUEjb1zheEk=',NULL,0,'尉迟涛','','','yuchitao@sports.cn',0,1,'2025-12-09 09:49:22.189456','尉迟涛','17045678901','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-09 09:49:22.189456','2026-02-03 03:02:49.681455'),(44,'pbkdf2_sha256$720000$qvhNxho6kQIjLuQESmM7Nz$90F114s/PP6irohYzxYr1ziJLNpLD5o2EQz3fOrsn+Y=',NULL,0,'邓浩然','','','denghaoran@sports.cn',0,1,'2025-12-10 17:25:09.652893','邓浩然','17156789012','athlete','',NULL,'1995-01-01','110105199501015571',NULL,NULL,NULL,NULL,0,'2025-12-10 17:25:09.652893','2026-02-03 03:02:49.681870'),(45,'pbkdf2_sha256$720000$qjTtdNuFbGJgL7hNR0Hdkp$RANERrRAUfNrCn6WpwGjBkJdwIvaG8LuckDdBZYD7HU=',NULL,0,'彭瑞','','','pengrui@sports.cn',0,1,'2025-12-10 22:42:33.249561','彭瑞','18067890123','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-10 22:42:33.249561','2026-02-03 03:02:49.682320'),(46,'pbkdf2_sha256$720000$F5OSmeFZeh6PGi5wIKkxbf$DN9J+JNfBNhlqgKiI0FEfR8SyJM/COkSly4jXgiQM6U=',NULL,0,'诸葛瑞','','','zhuguirui@sports.cn',0,1,'2025-12-12 02:19:09.785428','诸葛瑞','18978901234','athlete','',NULL,'1995-01-01','110105199501010279',NULL,NULL,NULL,NULL,0,'2025-12-12 02:19:09.785428','2026-02-03 03:02:49.682766'),(47,'pbkdf2_sha256$720000$wLo8kjyBXPdrdNBX6OVQji$TybYuHeKyinbfms35NlxQVSP0f9YZepZV1rp4qaVwjE=',NULL,0,'曾雨桐','','','zengyutong@sports.cn',0,1,'2025-12-13 06:55:33.652189','曾雨桐','19189012345','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-13 06:55:33.652189','2026-02-03 03:02:49.683170'),(48,'pbkdf2_sha256$720000$wBAVr3Aaw4ZBjMaJDmvW7q$/Z+Q4WguKblE23ZOaIWoyVFh4Ra4Wdq4mE1iovWfVok=',NULL,0,'肖强','','','xiaoqiang@sports.cn',0,1,'2025-12-14 11:32:09.789456','肖强','19290123456','athlete','',NULL,'1995-01-01','110105199501012055',NULL,NULL,NULL,NULL,0,'2025-12-14 11:32:09.789456','2026-02-03 03:02:49.683537'),(49,'pbkdf2_sha256$720000$s4BIN2PIdK68TAuvFULDlE$N/yf2SCbnpJoVAHiIiGX2F3BW9q3lMhwRSifafOQOvs=',NULL,0,'闻人敏','','','wenrenmin@sports.cn',0,1,'2025-12-15 16:09:33.652189','闻人敏','13801234567','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-15 16:09:33.652189','2026-02-03 03:02:49.684004'),(50,'pbkdf2_sha256$720000$FhXcdZSAx26axNdV13iVHa$SZWXlVzzSe/ElXDS3dZ5C0JnsIqq8v9ocx9oSg13TnU=',NULL,0,'田思琪','','','tiansiqi@sports.cn',0,1,'2025-12-15 21:45:22.189456','田思琪','13912345678','athlete','',NULL,'1995-01-01','110105199501018617',NULL,NULL,NULL,NULL,0,'2025-12-15 21:45:22.189456','2026-02-03 03:02:49.684477'),(51,'pbkdf2_sha256$720000$tQWrXFq3CWxEyhE7AqsO3s$dLnEpMau0LfwIL4Fq1jJgDUXPOfO/DGBek8KeFIAIfA=',NULL,0,'董悦','','','dongyue@sports.cn',0,1,'2025-12-17 01:32:09.652893','董悦','15023456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-17 01:32:09.652893','2026-02-03 03:02:49.684925'),(52,'pbkdf2_sha256$720000$VwGiQb4kFZzPqG4rsXsS3y$jYtqswPo3+Y86ZRWN4YwK9symPgR4TI5vTAqCIpxRfg=',NULL,0,'赫连峰','','','helianfeng@sports.cn',0,1,'2025-12-18 06:09:33.249561','赫连峰','15934567890','athlete','',NULL,'1995-01-01','110105199501016275',NULL,NULL,NULL,NULL,0,'2025-12-18 06:09:33.249561','2026-02-03 03:02:49.685486'),(53,'pbkdf2_sha256$720000$x2mbIwWw3GjgikhnjjHMrb$LQiI6isPMy0ew18O237VmpEZdjPqyER3O9HoEl/ApD8=',NULL,0,'袁一诺','','','yuanyinuo@sports.cn',0,1,'2025-12-19 10:46:09.785428','袁一诺','17845678901','athlete','',NULL,'1995-01-01','110105199501015942',NULL,NULL,NULL,NULL,0,'2025-12-19 10:46:09.785428','2026-02-03 03:02:49.686021'),(54,'pbkdf2_sha256$720000$IJLHt8oiNHVNjILEss3Ilm$xRZ8WDn87aAPBPwkrCuAS6xrjLhRFXKU4w+2/8Fllgs=',NULL,0,'潘明','','','panming@sports.cn',0,1,'2025-12-20 16:22:33.652189','潘明','18856789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-20 16:22:33.652189','2026-02-03 03:02:49.686567'),(55,'pbkdf2_sha256$720000$WmBnmVw0OIVe1DZbbmFDhu$n2PvZ79u3MalsheYY4+Yz/6o3Rugu+nxf1Ctwcq8/+4=',NULL,0,'澹台欣','','','tantaixin@sports.cn',0,1,'2025-12-20 22:59:22.189456','澹台欣','19967890123','athlete','',NULL,'1995-01-01','11010519950101291X',NULL,NULL,NULL,NULL,0,'2025-12-20 22:59:22.189456','2026-02-03 03:02:49.687100'),(56,'pbkdf2_sha256$720000$R6JONhJ9KVX52xhZBxCbmy$WL6qajpAEBSfkvD/GF2qqTEFchv9V5C06R2PMf9sVCA=',NULL,0,'于梓轩','','','yuzixuan@sports.cn',0,1,'2025-12-22 02:36:09.652893','于梓轩','13778901234','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-22 02:36:09.652893','2026-02-03 03:02:49.687567'),(57,'pbkdf2_sha256$720000$aY9KfjzUBxg7oCk61uK7vu$UCMlvrykGWXGcY+r3aJXjmFz2GBdCJFmmAqHUZtlkFw=',NULL,0,'蒋静','','','jiangjing@sports.cn',0,1,'2025-12-23 07:12:33.249561','蒋静','13689012345','athlete','',NULL,'1995-01-01','110105199501010033',NULL,NULL,NULL,NULL,0,'2025-12-23 07:12:33.249561','2026-02-03 03:02:49.688146'),(58,'pbkdf2_sha256$720000$A9YIQzl1bKvgtIIL9qwiLj$mHduASoU2LBmIwn/jfpAShCHn1BUMntyjAwt+czjiwU=',NULL,0,'慕容杰','','','murongjie@sports.cn',0,1,'2025-12-24 11:49:09.785428','慕容杰','14790123456','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-24 11:49:09.785428','2026-02-03 03:02:49.688607'),(59,'pbkdf2_sha256$720000$4eGS42SftcfKHsLBVqR673$FdRmE1upgGitB0x0gUrVSzs1GxGt/xwVx+HkFMoiIIU=',NULL,0,'蔡浩然','','','caihaoran@sports.cn',0,1,'2025-12-25 16:26:33.652189','蔡浩然','14501234567','athlete','',NULL,'2001-03-14','110105200103149641',NULL,NULL,NULL,NULL,0,'2025-12-25 16:26:33.652189','2026-02-03 03:02:49.689116'),(60,'pbkdf2_sha256$720000$ffkZs8NLNcN2FxMA8slpgX$l4VCeJeGqGBG/NdXRu2qUZFg4g0Mrc7HzoMrWsVu71c=',NULL,0,'余芳','','','yufang@sports.cn',0,1,'2025-12-25 21:23:22.189456','余芳','15112345678','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-25 21:23:22.189456','2026-02-03 03:02:49.689653'),(61,'pbkdf2_sha256$720000$wNCBX44yvWMGXLAbMB1uks$7XEGKZ7MfKCQWkt69AFBLeMnqV4JsLU6TGDMJe+UyLs=',NULL,0,'上官琪','','','shangguanqi@sports.cn',0,1,'2025-12-27 01:40:09.652893','上官琪','15823456789','athlete','',NULL,'1995-01-01','110105199501012493',NULL,NULL,NULL,NULL,0,'2025-12-27 01:40:09.652893','2026-02-03 03:02:49.690152'),(62,'pbkdf2_sha256$720000$H4meqYpj9BuNi7MyY6EAgK$Kol6FB/rQgBhQZNs0dc7Q+A+rk47LXUrxE3UbO617og=',NULL,0,'杜泽宇','','','duzeyu@sports.cn',0,1,'2025-12-28 06:17:33.249561','杜泽宇','17734567890','athlete','',NULL,'1995-01-01','110105199501015387',NULL,NULL,NULL,NULL,0,'2025-12-28 06:17:33.249561','2026-02-03 03:02:49.690621'),(63,'pbkdf2_sha256$720000$r2t4vmFCkTdbIHwlUK7cMh$HixdQead/j6DVBnMvf9OFJIo7g3T0zoXLmlh60kbk20=',NULL,0,'苏涛','','','sutao@sports.cn',0,1,'2025-12-29 10:54:09.785428','苏涛','18745678901','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-29 10:54:09.785428','2026-02-03 03:02:49.691126'),(64,'pbkdf2_sha256$720000$8el6QqaeQrsAJdNFZCYhIM$FnoZ4SsqWKCMq4SwfPALHFe7gQa8g/mkpQVL9hge+kc=',NULL,0,'皇甫明','','','huangfuming@sports.cn',0,1,'2025-12-30 16:31:33.652189','皇甫明','19856789012','athlete','',NULL,'1995-01-01','110105199501011108',NULL,NULL,NULL,NULL,0,'2025-12-30 16:31:33.652189','2026-02-03 03:02:49.691577'),(65,'pbkdf2_sha256$720000$LeH72NMv0bptajWntX24bR$CcLG1DA+NN+ZVL4+jL0IOJFMf7hzL8BXOG6j7EcvAGU=',NULL,0,'叶思琪','','','yesiqi@sports.cn',0,1,'2025-12-30 22:08:22.189456','叶思琪','13567890123','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-30 22:08:22.189456','2026-02-03 03:02:49.692082'),(66,'pbkdf2_sha256$720000$dGyB5Zentwe6WNhL6OBWub$xBmxy1UY84ITsz+NEArmVC2zz733k093NgqF6LAs9rY=',NULL,0,'吕悦','','','lvyue@sports.cn',0,1,'2026-01-01 01:45:09.652893','吕悦','13478901234','athlete','',NULL,'1995-01-01','11010519950101267X',NULL,NULL,NULL,NULL,0,'2026-01-01 01:45:09.652893','2026-02-03 03:02:49.693483'),(67,'pbkdf2_sha256$720000$oraAj7ilaW9R7kBiXHRKZ8$HDREO9QihnuKUztRgtjLwRrJ2vD1CEVF6HhFHp5Sp04=',NULL,0,'司马阳','','','simayang@sports.cn',0,1,'2026-01-02 06:22:33.249561','司马阳','15289012345','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-02 06:22:33.249561','2026-02-03 03:02:49.694023'),(68,'pbkdf2_sha256$720000$Na0oFPYOgSXn6yUNAdRazA$hIaflV2SG9jT9IYaxnyFUdnm3F++vdYr95QG6v6RvsY=',NULL,0,'魏一诺','','','weiyinuo@sports.cn',0,1,'2026-01-03 10:59:09.785428','魏一诺','15790123456','athlete','',NULL,'1995-01-01','110105199501017876',NULL,NULL,NULL,NULL,0,'2026-01-03 10:59:09.785428','2026-02-03 03:02:49.694512'),(69,'pbkdf2_sha256$720000$p87wnTx9rGl0pzhWOkdkZW$hC8uJVuhUu9QB6Kiv8iAACGkDKeERYbStyAguuyPytA=',NULL,0,'薛强','','','xueqiang@sports.cn',0,1,'2026-01-04 16:36:33.652189','薛强','17601234567','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-04 16:36:33.652189','2026-02-03 03:02:49.695090'),(70,'pbkdf2_sha256$720000$rDOSXP01DWermWKld74mzg$oF692QPE4nvCL9WwkDPbRlKBXkH/ispkUBR5DtWNm1w=',NULL,0,'长孙佳','','','zhangsunjia@sports.cn',0,1,'2026-01-04 22:13:22.189456','长孙佳','18612345678','athlete','',NULL,'1995-01-01','110105199501013234',NULL,NULL,NULL,NULL,0,'2026-01-04 22:13:22.189456','2026-02-03 03:02:49.695778'),(71,'pbkdf2_sha256$720000$Xet1zxKJWEOi8yPPLprHZD$xkTZBn3/PNXEX4ItBGlgvxMxaDB2ko2fOLpBsNfmjuM=',NULL,0,'金梓轩','','','jinzixuan@sports.cn',0,1,'2026-01-06 01:50:09.652893','金梓轩','19723456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-06 01:50:09.652893','2026-02-03 03:02:49.696331'),(72,'pbkdf2_sha256$720000$mNQ7oWcwEHcRscV49EMaOo$6BupR5H/SyEGQXHKnb+CqLcu0QNVWaUIqNsbhILNBUg=',NULL,0,'陆静','','','lujing@sports.cn',0,1,'2026-01-07 06:27:33.249561','陆静','13334567890','athlete','',NULL,'1995-01-01','110105199501018465',NULL,NULL,NULL,NULL,0,'2026-01-07 06:27:33.249561','2026-02-03 03:02:49.696959'),(73,'pbkdf2_sha256$720000$Mw8Y99nziO9JFhXModaAuC$Fkl5YqOkPNAZXbx6Ess3NpquIl6Legr/BdMo1YvLScI=',NULL,0,'尉迟悦','','','yuchiyue@sports.cn',0,1,'2026-01-08 10:24:09.785428','尉迟悦','13245678901','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-08 10:24:09.785428','2026-02-03 03:02:49.697642'),(74,'pbkdf2_sha256$720000$tsAImrK8oE5973rWh64N8g$8xlNp8VjHUSN3O5sRl/3BVpQlWmAWNik/Oa5fDfDbYE=',NULL,0,'夏浩然','','','xiahaoran@sports.cn',0,1,'2026-01-09 16:41:33.652189','夏浩然','15356789012','athlete','',NULL,'1995-01-01','110105199501011685',NULL,NULL,NULL,NULL,0,'2026-01-09 16:41:33.652189','2026-02-03 03:02:49.698177'),(75,'pbkdf2_sha256$720000$oh0dP99MshmognE4NUhqnR$/ed+kY7xc98UFYwf4PIycqSdxBcBupm2pI1t15sA4cw=',NULL,0,'钟芳','','','zhongfang@sports.cn',0,1,'2026-01-09 22:18:22.189456','钟芳','15667890123','athlete','',NULL,'1995-01-01','110105199501016996',NULL,NULL,NULL,NULL,0,'2026-01-09 22:18:22.189456','2026-02-03 03:02:49.698693'),(76,'pbkdf2_sha256$720000$diKelInTj6SNrHEtFF9AuW$Vwi5GE98lnIjsI3XYyh72TQAHDqbHRJpWrKNmbZrYuE=',NULL,0,'诸葛敏','','','zhuguimin@sports.cn',0,1,'2026-01-11 01:55:09.652893','诸葛敏','17578901234','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-11 01:55:09.652893','2026-02-03 03:02:49.699279'),(77,'pbkdf2_sha256$720000$6vZW2jJTepPDlbLyG9fYKh$GNYUGUCx0OtWynxHDP7PMgfsR3xbXVb8CX6opk0MU+M=',NULL,0,'汪泽宇','','','wangzeyu@sports.cn',0,1,'2026-01-12 06:32:33.249561','汪泽宇','18589012345','athlete','',NULL,'1995-01-01','110105199501012231',NULL,NULL,NULL,NULL,0,'2026-01-12 06:32:33.249561','2026-02-03 03:02:49.699796'),(78,'pbkdf2_sha256$720000$rZG8lv7SahIVUtlE92DiTp$lfatNo/YjNv1Cc+kywPFO+c4uip4VkqLKPFA7igMfxM=',NULL,0,'田涛','','','tiantao@sports.cn',0,1,'2026-01-13 10:29:09.785428','田涛','19690123456','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-13 10:29:09.785428','2026-02-03 03:02:49.700299'),(79,'pbkdf2_sha256$720000$L7UeKNdcejeCr5NIO6LI0p$OBg15PorAky6TeAfTFXBuBsRGxad66cdbdAXnmFkXv4=',NULL,0,'欧阳雪','','','ouyangxue@sports.cn',0,1,'2026-01-14 16:46:33.652189','欧阳雪','13101234567','athlete','',NULL,'1995-01-01','11010519950101574X',NULL,NULL,NULL,NULL,0,'2026-01-14 16:46:33.652189','2026-02-03 03:02:49.700975'),(80,'pbkdf2_sha256$720000$MfqarAE74Vacw0ccK9ptkx$TapcaJxKLYI5B7iqWybAj1ny4A07U6uBvY7Iffk1KxA=',NULL,0,'董思琪','','','dongsiqi@sports.cn',0,1,'2026-01-14 22:23:22.189456','董思琪','13012345678','athlete','',NULL,'1995-01-01','110105199501018211',NULL,NULL,NULL,NULL,0,'2026-01-14 22:23:22.189456','2026-02-03 03:02:49.701480'),(81,'pbkdf2_sha256$720000$iGlLTzWGi8tsnacWOPe7O9$cBwA7EJn7SYWfgscaWrKmBwHTOVeeya7bAauKiLz5vM=',NULL,0,'袁悦','','','yuanyue@sports.cn',0,1,'2026-01-16 01:20:09.652893','袁悦','14923456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-16 01:20:09.652893','2026-02-03 03:02:49.701973'),(82,'pbkdf2_sha256$720000$dh4GQfqDmxROrkxqeag0Gp$jnUO/aZSF6F+QV5nF8jCaxatGSSJiGc5h1okGSRuDfQ=',NULL,0,'澹台泽宇','','','tantaizeyu@sports.cn',0,1,'2026-01-17 06:37:33.249561','澹台泽宇','17034567890','athlete','',NULL,'1995-01-01','110105199501016910',NULL,NULL,NULL,NULL,0,'2026-01-17 06:37:33.249561','2026-02-03 03:02:49.702459'),(83,'pbkdf2_sha256$720000$gdaX9mOgEiG3YD4JEC6sex$GRmu/txwqc2YU+NjIoxUYT0dVT3xtkDACA/Ti6U3yls=',NULL,0,'潘一诺','','','panyinuo@sports.cn',0,1,'2026-01-18 11:14:09.785428','潘一诺','17145678901','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-18 11:14:09.785428','2026-02-03 03:02:49.702941'),(84,'pbkdf2_sha256$720000$QkmI4i5KmV8E52uceP7a3D$JXJR5+ldoNQ/VJ9KUJKAe/BUH30BR/pJIRdrVNV5YnE=',NULL,0,'于强','','','yuqiang@sports.cn',0,1,'2026-01-19 16:51:33.652189','于强','18056789012','athlete','',NULL,'1995-01-01','110105199501014931',NULL,NULL,NULL,NULL,0,'2026-01-19 16:51:33.652189','2026-02-03 03:02:49.703353'),(85,'pbkdf2_sha256$720000$A19FJFLhAwnx1Tm79x61JQ$6VDThznmYeIAS00dE4i5G5cqVBwrMJvwOsg3u7hQYu8=',NULL,0,'蒋梓轩','','','jiangzixuan@sports.cn',0,1,'2026-01-19 22:28:22.189456','蒋梓轩','18967890123','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-19 22:28:22.189456','2026-02-03 03:02:49.703727'),(86,'pbkdf2_sha256$720000$tYEMopQ1wxL4bR8LmkwiIQ$oJCBIoeuvAz0J/Yt9LxozOZnPUQZ2OSskvbC/WLb9t0=',NULL,0,'蔡静','','','caijing@sports.cn',0,1,'2026-01-21 02:05:09.652893','蔡静','19178901234','athlete','',NULL,'1997-06-01','110105199706017642',NULL,NULL,NULL,NULL,0,'2026-01-21 02:05:09.652893','2026-02-03 03:02:49.704227'),(87,'pbkdf2_sha256$720000$Zs1a4YIFJRgxpxyHC2KTga$p2tDX6pceiGqiPRdgBIA8hhLgKXwWYr1d9SLmzCC3jo=',NULL,0,'余浩然','','','yuhaoran@sports.cn',0,1,'2026-01-22 06:42:33.249561','余浩然','19289012345','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-22 06:42:33.249561','2026-02-03 03:02:49.704821'),(88,'pbkdf2_sha256$720000$DZtIbIepo51IJzQXVRwZ5F$47wBfdSaOscEHa2KiZuCTbcaQucH/We2o+It1TDDOZM=',NULL,0,'慕容琪','','','murongqi@sports.cn',0,1,'2026-01-23 11:19:09.785428','慕容琪','13890123456','athlete','',NULL,'1995-01-01','110105199501013787',NULL,NULL,NULL,NULL,0,'2026-01-23 11:19:09.785428','2026-02-03 03:02:49.705476'),(89,'pbkdf2_sha256$720000$IvsQVEXSelTVvYeOs6lvS5$S2FeBf5IaKPeHcqfliCkAeCvgZCgQKirARssWECyAP8=','2026-02-03 08:37:40.610981',0,'苏思琪','','','susiqi@sports.cn',0,1,'2026-01-24 16:56:33.652189','苏思琪','13901234567','athlete','',NULL,'1995-01-01','110105199501011757',NULL,NULL,NULL,NULL,0,'2026-01-24 16:56:33.652189','2026-02-03 03:02:49.706087'),(90,'pbkdf2_sha256$720000$gAUfT2ll4VsN7hlFYqHm6o$zZn2ryz0d0xfE/Q5FiSHGw3sv3GEursPw38i0MRFkgs=',NULL,0,'杜悦','','','duyue@sports.cn',0,1,'2026-01-24 22:33:22.189456','杜悦','15012345678','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-24 22:33:22.189456','2026-02-03 03:02:49.706679'),(91,'pbkdf2_sha256$720000$YzshThXWe4qAz9XmFczorm$iSpWaG4cVp9FMjH0ViT+UyNNLfmIGFKksZXlk806nnM=','2026-02-03 07:51:18.367455',0,'叶泽宇','','','yezeyu@sports.cn',0,1,'2026-01-26 02:10:09.652893','叶泽宇','15923456789','athlete','',NULL,'1995-01-01','110105199501019556',NULL,NULL,NULL,NULL,0,'2026-01-26 02:10:09.652893','2026-02-03 03:02:49.707295'),(92,'pbkdf2_sha256$720000$uxmyApo6XOp5CcUmtQt4fl$ni8pm0LhS6aRGkGJFRq/fyAVqnynmb0j7+F/UGK25Sg=',NULL,0,'皇甫佳','','','huangfujia@sports.cn',0,1,'2026-01-27 06:47:33.249561','皇甫佳','17834567890','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-27 06:47:33.249561','2026-02-03 03:02:49.707847'),(93,'pbkdf2_sha256$720000$eweM4uVgqca6Au2aJ5wlUH$viS8qv9ajmNJ0nKYxi33PUs9ltsBtMWdILbdgJsCkTY=','2026-02-03 07:50:57.928378',0,'吕一诺','','','lvyinuo@sports.cn',0,1,'2026-01-28 11:24:09.785428','吕一诺','18845678901','athlete','',NULL,'1995-01-01','110105199501018393',NULL,NULL,NULL,NULL,0,'2026-01-28 11:24:09.785428','2026-02-03 03:02:49.708463'),(94,'pbkdf2_sha256$720000$Jgzfe9DUbNn2ISCg4abWGB$G2CvdHfxsELiwbdPb5Ta3NyKXhtkLlmHPGSyDsK7PpI=',NULL,0,'魏强','','','weiqiang@sports.cn',0,1,'2026-01-29 16:21:33.652189','魏强','19956789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-29 16:21:33.652189','2026-02-03 03:02:49.709101'),(95,'pbkdf2_sha256$720000$GD7VpbOd5xgKngOiGfC3hL$6Ll1UFZh9gS3fQDoTISmcbSrAYaDDqo05AEl53d3fX8=','2026-02-03 07:49:26.179273',0,'薛梓轩','','','xuezixuan@sports.cn',0,1,'2026-01-29 22:38:22.189456','薛梓轩','13767890123','athlete','',NULL,'1995-01-01','110105199501017067',NULL,NULL,NULL,NULL,0,'2026-01-29 22:38:22.189456','2026-02-03 03:02:49.709786'),(96,'pbkdf2_sha256$720000$vNuiyy19GgEaqGIzTxdeIm$6xKS+RkGYwjfhp4MDBhz80JNYdtVNPz3cKCxlurvQ0k=','2026-02-03 07:49:05.014138',0,'金静','','','jinjing@sports.cn',0,1,'2026-01-30 03:15:09.652893','金静','13678901234','athlete','',NULL,'1995-01-01','110105199501013293',NULL,NULL,NULL,NULL,0,'2026-01-30 03:15:09.652893','2026-02-03 03:02:49.710383'),(97,'pbkdf2_sha256$720000$4z55hsJwBdzAKYFdaNNX6o$JrLqAlrp1wmEVrgzAInbMMVpCTAMOfn4HeUpDJ1h1/s=','2026-02-03 07:48:44.665840',0,'司马杰','','','simajie@sports.cn',0,1,'2026-01-30 07:52:33.249561','司马杰','14789012345','athlete','',NULL,'1995-01-01','110105199501011335',NULL,NULL,NULL,NULL,0,'2026-01-30 07:52:33.249561','2026-02-03 03:02:49.711027'),(98,'pbkdf2_sha256$720000$KLQosZl7HmrhAajryNejfl$D2a8Y5rw1U4J3/VdzzWLEITz4nccb+UdroLTc6V02oA=','2026-02-03 07:48:22.656616',0,'陆思琪','','','lusiqi@sports.cn',0,1,'2026-01-30 12:29:09.785428','陆思琪','14590123456','athlete','',NULL,'1995-01-01','110105199501013963',NULL,NULL,NULL,NULL,0,'2026-01-30 12:29:09.785428','2026-02-03 03:02:49.711602'),(99,'pbkdf2_sha256$720000$KMSeCWBE3XahdFYUYGdXEr$kRgD96siu/4aGli/8Q+mDbd6EPhsWQV+x4QKSsdBFyI=',NULL,0,'夏悦','','','xiayue@sports.cn',0,1,'2026-01-30 17:06:33.652189','夏悦','15101234567','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-30 17:06:33.652189','2026-02-03 03:02:49.712147'),(100,'pbkdf2_sha256$720000$rjREs8coWof2w5iT1or1MT$564Xu+GJ3WGCEiC/fLTEWCPTH+G4SNZh1eL5/emEmcs=','2026-02-03 07:47:57.641464',0,'尉迟浩然','','','yuchihaoran@sports.cn',0,1,'2026-01-30 22:43:22.189456','尉迟浩然','15812345678','athlete','',NULL,'1995-01-01','110105199501015539',NULL,NULL,NULL,NULL,0,'2026-01-30 22:43:22.189456','2026-02-03 03:02:49.712688'),(101,'pbkdf2_sha256$720000$n4zzi6vu5RqpEZEWoXPNHm$L2ptEbfv8LkTQ2uXVsgz1+vL7mP2SlCBlh9yHIlFPbc=',NULL,0,'钟泽宇','','','zhongzeyu@sports.cn',0,1,'2026-01-31 02:20:09.652893','钟泽宇','17723456789','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-31 02:20:09.652893','2026-02-03 03:02:49.713306'),(102,'pbkdf2_sha256$720000$XdFgmbnYqjOvF88YCRFIWH$BoNmsJaWJQYzD24ua0qUKSxT0flootSb7/TMtUgTAYM=',NULL,0,'汪静','','','wangjing@sports.cn',0,1,'2026-01-31 06:57:33.249561','汪静','18734567890','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-31 06:57:33.249561','2026-02-03 03:02:49.713801'),(103,'pbkdf2_sha256$720000$TKOz8RqNUmy8WiyTj5pmFW$ZvZpm9SkPzayrIV27rhRgxcsC/igeRtvRn8ww2nbOj4=',NULL,0,'田一诺','','','tianyinuo@sports.cn',0,1,'2026-01-31 11:34:09.785428','田一诺','19845678901','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-31 11:34:09.785428','2026-02-03 03:02:49.714281'),(104,'pbkdf2_sha256$720000$OH2ghqS3rvbCFO9VR5D3Z2$mpwzSkur63wZQwpfaMXmQt9i9TcFncpigIWcUs38lxc=','2026-02-03 06:49:07.264966',0,'上官强','','','shangguanqiang@sports.cn',0,1,'2026-01-31 15:59:59.999999','上官强','13556789012','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-31 15:59:59.999999','2026-02-03 03:02:49.714812'),(105,'pbkdf2_sha256$720000$Uju1qCxDo2ZFVtwFnIxBbv$amrKR1U1eYPmieeaxmwpupu2O232qCanJlwKchXYFDo=',NULL,0,'曾梓轩','','','zengzixuan@sports.cn',0,1,'2025-11-05 08:54:22.189456','曾梓轩','13467890123','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-05 08:54:22.189456','2026-02-03 03:02:49.715302'),(106,'pbkdf2_sha256$720000$0KGXf3AOS9qbFlPFSMP7Xx$UdEDRzL9r/BX0Pomoj7wZnumzwrqyOKC/4hF2OxTZfM=',NULL,0,'肖思琪','','','xiaosiqi@sports.cn',0,1,'2025-11-12 16:31:33.652189','肖思琪','15278901234','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-12 16:31:33.652189','2026-02-03 03:02:49.715810'),(107,'pbkdf2_sha256$720000$XFvJ0Ukraap3edyUU9223c$xf9vsRKP3Ok9/rm5+k2QcUq6eGLClYfSEyCumUa9GKs=',NULL,0,'彭悦','','','pengyue@sports.cn',0,1,'2025-11-19 19:07:22.189456','彭悦','15789012345','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-19 19:07:22.189456','2026-02-03 03:02:49.716260'),(108,'pbkdf2_sha256$720000$80fIhII2CK6g7Y2CQXo7Hd$cOYXXG+2JdhRHW4ZHyYnnEWjJEsIhKvkJQCZqRFiN/Y=',NULL,0,'诸葛泽宇','','','zhuguizeyu@sports.cn',0,1,'2025-12-06 22:44:09.652893','诸葛泽宇','17690123456','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-06 22:44:09.652893','2026-02-03 03:02:49.716663'),(109,'pbkdf2_sha256$720000$3RZagnd1PEnyjekQHdHzdj$JfCy5KqYyvJ9vl3/5bKDLyjTztQ9VwACvuP/ajsTWY0=','2026-02-03 01:53:53.093664',0,'邓强','','','dengqiang@sports.cn',0,1,'2025-12-14 03:21:33.249561','邓强','18601234567','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-14 03:21:33.249561','2026-02-03 03:02:49.717139'),(110,'pbkdf2_sha256$720000$8dB44yOQbYpDKTYNnoK4eZ$+dR2xVODd0pVKAlDGYjQzXFneTLYa6kFZdSMpRW+2vI=',NULL,0,'刘凯','','','liukai@sports.cn',0,1,'2025-12-21 07:57:09.785428','刘凯','13822556688','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-21 07:57:09.785428','2026-02-03 03:02:49.717737'),(111,'pbkdf2_sha256$720000$QsF8MShyGBH79UzlGWqiu9$xLh4W/qEMGJdbJIxJiFOZFAbkuprUW+eubatxPuGa5Q=',NULL,0,'王梓涵','','','wangzihan@sports.cn',0,1,'2025-12-28 12:34:33.652189','王梓涵','15933669900','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-28 12:34:33.652189','2026-02-03 03:02:49.718288'),(112,'pbkdf2_sha256$720000$aZovHJPllES5Ns6GgBeEtQ$W09sqpf4zEXK707cvIqEVz7UJYpQXahJrtZFkvwcNwg=','2026-02-15 07:05:48.151271',0,'陈玥','','','chenyue@sports.cn',0,1,'2026-01-05 18:11:22.189456','陈玥','17811447799','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-05 18:11:22.189456','2026-02-03 03:02:49.718804'),(113,'pbkdf2_sha256$720000$I2izZSJgd84MYXfMib6xLX$5PsvlsZKKk50RpYawhcb4bwyMLEPkVx5ZOZiJu0cUss=',NULL,0,'李沐宸','','','limuchen@sports.cn',0,1,'2026-01-11 21:47:09.652893','李沐宸','18855228800','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-11 21:47:09.652893','2026-02-03 03:02:49.719332'),(114,'pbkdf2_sha256$720000$zqAnYP3rWqmBBBvd3TIhG1$E9tK6KpQEQfwIFjNehxEl8tBvbFF2qN475aG0G5sKmU=',NULL,0,'赵峰','','','zhaofeng@sports.cn',0,1,'2026-01-19 02:24:33.249561','赵峰','19966339911','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-19 02:24:33.249561','2026-02-03 03:02:49.719844'),(115,'pbkdf2_sha256$720000$psqfZ1laozhin1k2C1YAgg$rQbqHX+3VRn35CFPNVd1sZVdcUqPn6fTjqFPYV/z1gQ=',NULL,0,'张语桐','','','zhangyutong@sports.cn',0,1,'2026-01-26 06:21:09.785428','张语桐','13744882266','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-26 06:21:09.785428','2026-02-03 03:02:49.720525'),(116,'pbkdf2_sha256$720000$9BbNWYgGIpNYbVNgSnqkVE$aHmdoSu9Wy8TiqIxmCEtMi+nSPoSUeugEVtSxFROWEw=',NULL,0,'黄莉','','','huangli@sports.cn',0,1,'2025-11-27 23:18:09.652893','黄莉','13677225588','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-11-27 23:18:09.652893','2026-02-03 03:02:49.721204'),(117,'pbkdf2_sha256$720000$gBnWXYqpY6VxSX7f9EjFz6$0Rb9nVU2fKNSPjzDjOHHW+HUCRhtePhgSOg520jVLi4=',NULL,0,'周奕辰','','','zhouyichen@sports.cn',0,1,'2025-12-15 03:55:33.249561','周奕辰','14788114499','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2025-12-15 03:55:33.249561','2026-02-03 03:02:49.721832'),(118,'pbkdf2_sha256$720000$P8FblWzPhCSBmolYOgtr28$Io2w3/mIS+/En67E0Y7DDtTyGfOfz9monJW24e48Qd0=',NULL,0,'吴娜','','','wuna@sports.cn',0,1,'2026-01-02 08:31:09.785428','吴娜','15199226633','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-02 08:31:09.785428','2026-02-03 03:02:49.722387'),(119,'pbkdf2_sha256$720000$CtsDIIsYlo6BBxz8mQk7L4$D56/eFjKOyyiPXj/lcIzl79OMLvym9VjI+PvDRZ+0/Y=',NULL,0,'孙泽宇','','','sunzeyu@sports.cn',0,1,'2026-01-29 13:08:33.652189','孙泽宇','15200337766','referee','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-01-29 13:08:33.652189','2026-02-03 03:02:49.722921'),(120,'pbkdf2_sha256$720000$XGv9tIr6Sp99MsYDLJgJMb$1VkCFrBwWI+a0x67JZ/0HuQbC/4TM+ry9AegjEfo5Sw=','2026-02-15 09:20:22.863817',0,'王小明','','','wxm@sports.cn',0,1,'2026-02-15 06:57:39.069425','王生生','13287963401','athlete','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-02-15 06:57:39.296062','2026-02-15 06:58:40.860974');
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

-- Dump completed on 2026-02-15 22:50:12
