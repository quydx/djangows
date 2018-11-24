-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: backup_core2
-- ------------------------------------------------------
-- Server version	5.7.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add Token',1,'add_token'),(2,'Can change Token',1,'change_token'),(3,'Can delete Token',1,'delete_token'),(4,'Can add attr',2,'add_attr'),(5,'Can change attr',2,'change_attr'),(6,'Can delete attr',2,'delete_attr'),(7,'Can add attr value',3,'add_attrvalue'),(8,'Can change attr value',3,'change_attrvalue'),(9,'Can delete attr value',3,'delete_attrvalue'),(10,'Can add backup',4,'add_backup'),(11,'Can change backup',4,'change_backup'),(12,'Can delete backup',4,'delete_backup'),(13,'Can add file',5,'add_file'),(14,'Can change file',5,'change_file'),(15,'Can delete file',5,'delete_file'),(16,'Can add file data',6,'add_filedata'),(17,'Can change file data',6,'change_filedata'),(18,'Can delete file data',6,'delete_filedata'),(19,'Can add file sys',7,'add_filesys'),(20,'Can change file sys',7,'change_filesys'),(21,'Can delete file sys',7,'delete_filesys'),(22,'Can add key user',8,'add_keyuser'),(23,'Can change key user',8,'change_keyuser'),(24,'Can delete key user',8,'delete_keyuser'),(25,'Can add log entry',9,'add_logentry'),(26,'Can change log entry',9,'change_logentry'),(27,'Can delete log entry',9,'delete_logentry'),(28,'Can add permission',10,'add_permission'),(29,'Can change permission',10,'change_permission'),(30,'Can delete permission',10,'delete_permission'),(31,'Can add group',11,'add_group'),(32,'Can change group',11,'change_group'),(33,'Can delete group',11,'delete_group'),(34,'Can add user',12,'add_user'),(35,'Can change user',12,'change_user'),(36,'Can delete user',12,'delete_user'),(37,'Can add content type',13,'add_contenttype'),(38,'Can change content type',13,'change_contenttype'),(39,'Can delete content type',13,'delete_contenttype'),(40,'Can add session',14,'add_session'),(41,'Can change session',14,'change_session'),(42,'Can delete session',14,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$100000$aBZ63YYNajm9$rzm3GNi/nAXcJswlodWLf3MREsfCCjiQRNrvxtsI+eA=','2018-11-24 10:17:09.946758',1,'admin','','','',1,1,'2018-10-24 10:49:34.639071');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('f6a7d9168a63be96a7033204bd19be7d9fcba351','2018-10-24 10:51:04.560207',1);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-10-24 10:50:39.010233','2','bootcamp',1,'[{\"added\": {}}]',12,1),(2,'2018-10-24 10:51:00.928524','f16e68d691f08d649e9413d069b177bc561c6c65','f16e68d691f08d649e9413d069b177bc561c6c65',1,'[{\"added\": {}}]',1,1),(3,'2018-10-24 10:51:04.560640','f6a7d9168a63be96a7033204bd19be7d9fcba351','f6a7d9168a63be96a7033204bd19be7d9fcba351',1,'[{\"added\": {}}]',1,1),(4,'2018-10-26 20:29:01.225030','12','sanhok-2018-10-24 22:21:19',2,'[{\"changed\": {\"fields\": [\"host\"]}}]',4,1),(5,'2018-11-24 10:17:50.827581','2','bootcamp',3,'',12,1),(6,'2018-11-24 10:17:50.830750','3','sanhok',3,'',12,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'admin','logentry'),(11,'auth','group'),(10,'auth','permission'),(12,'auth','user'),(1,'authtoken','token'),(13,'contenttypes','contenttype'),(2,'rest','attr'),(3,'rest','attrvalue'),(4,'rest','backup'),(5,'rest','file'),(6,'rest','filedata'),(7,'rest','filesys'),(8,'rest','keyuser'),(14,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-10-24 10:49:07.757202'),(2,'auth','0001_initial','2018-10-24 10:49:08.448647'),(3,'admin','0001_initial','2018-10-24 10:49:08.607234'),(4,'admin','0002_logentry_remove_auto_add','2018-10-24 10:49:08.618216'),(5,'contenttypes','0002_remove_content_type_name','2018-10-24 10:49:08.745153'),(6,'auth','0002_alter_permission_name_max_length','2018-10-24 10:49:08.775000'),(7,'auth','0003_alter_user_email_max_length','2018-10-24 10:49:08.790204'),(8,'auth','0004_alter_user_username_opts','2018-10-24 10:49:08.800410'),(9,'auth','0005_alter_user_last_login_null','2018-10-24 10:49:08.884266'),(10,'auth','0006_require_contenttypes_0002','2018-10-24 10:49:08.891109'),(11,'auth','0007_alter_validators_add_error_messages','2018-10-24 10:49:08.906578'),(12,'auth','0008_alter_user_username_max_length','2018-10-24 10:49:08.995115'),(13,'auth','0009_alter_user_last_name_max_length','2018-10-24 10:49:09.058704'),(14,'authtoken','0001_initial','2018-10-24 10:49:09.149033'),(15,'authtoken','0002_auto_20160226_1747','2018-10-24 10:49:09.257584'),(16,'rest','0001_initial','2018-10-24 10:49:10.121152'),(17,'rest','0002_auto_20181023_2352','2018-10-24 10:49:10.155907'),(18,'rest','0003_auto_20181024_1027','2018-10-24 10:49:10.168815'),(19,'rest','0004_auto_20181024_1049','2018-10-24 10:49:10.183459'),(20,'sessions','0001_initial','2018-10-24 10:49:10.255485');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0l3yg5ulo22lmigs83nz74mzxikyxy23','ZDcxNmQ0ZjA5ZDM0MTI0Y2EwMjg4NDNhM2Y5MDhhNzA1YTU5MmI5Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NmI3MDE2MTE1ZDBkZWJmNzk3NDI3NGY0NmJhZmUwODk0OTIzYjdkIn0=','2018-11-09 19:57:57.097133'),('fdcr04w0k59y3ovtq5udq5kuygtvkicw','ZDcxNmQ0ZjA5ZDM0MTI0Y2EwMjg4NDNhM2Y5MDhhNzA1YTU5MmI5Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NmI3MDE2MTE1ZDBkZWJmNzk3NDI3NGY0NmJhZmUwODk0OTIzYjdkIn0=','2018-12-08 10:17:09.957180'),('lg0pmfxay175p03zl7ps59w3yshs05xf','ZDcxNmQ0ZjA5ZDM0MTI0Y2EwMjg4NDNhM2Y5MDhhNzA1YTU5MmI5Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NmI3MDE2MTE1ZDBkZWJmNzk3NDI3NGY0NmJhZmUwODk0OTIzYjdkIn0=','2018-11-09 20:43:06.123383'),('rnu8ledp83lzsgawew2523vnsqzkv7s8','ZDcxNmQ0ZjA5ZDM0MTI0Y2EwMjg4NDNhM2Y5MDhhNzA1YTU5MmI5Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NmI3MDE2MTE1ZDBkZWJmNzk3NDI3NGY0NmJhZmUwODk0OTIzYjdkIn0=','2018-11-07 10:50:03.978388'),('xm5oirnbi9xphvmtpiwvuggpc29y9n0d','ZDcxNmQ0ZjA5ZDM0MTI0Y2EwMjg4NDNhM2Y5MDhhNzA1YTU5MmI5Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NmI3MDE2MTE1ZDBkZWJmNzk3NDI3NGY0NmJhZmUwODk0OTIzYjdkIn0=','2018-11-07 10:52:41.194654');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_attr`
--

DROP TABLE IF EXISTS `rest_attr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_attr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type_attr` int(11) NOT NULL,
  `file_sys_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rest_attr_file_sys_id_af206b4c_fk_rest_filesys_id` (`file_sys_id`),
  CONSTRAINT `rest_attr_file_sys_id_af206b4c_fk_rest_filesys_id` FOREIGN KEY (`file_sys_id`) REFERENCES `rest_filesys` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_attr`
--

LOCK TABLES `rest_attr` WRITE;
/*!40000 ALTER TABLE `rest_attr` DISABLE KEYS */;
INSERT INTO `rest_attr` VALUES (1,'access_time',0,1),(2,'modify_time',0,1),(3,'create_time',0,1),(4,'uid',0,1),(5,'gid',0,1),(6,'mode',0,1),(7,'acl',0,1);
/*!40000 ALTER TABLE `rest_attr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_attrvalue`
--

DROP TABLE IF EXISTS `rest_attrvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_attrvalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attr_id` int(11) NOT NULL,
  `file_object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rest_attrvalue_attr_id_1c23e09b_fk_rest_attr_id` (`attr_id`),
  KEY `rest_attrvalue_file_object_id_87544327_fk_rest_file_id` (`file_object_id`),
  CONSTRAINT `rest_attrvalue_attr_id_1c23e09b_fk_rest_attr_id` FOREIGN KEY (`attr_id`) REFERENCES `rest_attr` (`id`),
  CONSTRAINT `rest_attrvalue_file_object_id_87544327_fk_rest_file_id` FOREIGN KEY (`file_object_id`) REFERENCES `rest_file` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1765 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_attrvalue`
--

LOCK TABLES `rest_attrvalue` WRITE;
/*!40000 ALTER TABLE `rest_attrvalue` DISABLE KEYS */;
/*!40000 ALTER TABLE `rest_attrvalue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_backup`
--

DROP TABLE IF EXISTS `rest_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `store_path` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `host` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rest_backup_user_id_bd1284f7_fk_auth_user_id` (`user_id`),
  CONSTRAINT `rest_backup_user_id_bd1284f7_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_backup`
--

LOCK TABLES `rest_backup` WRITE;
/*!40000 ALTER TABLE `rest_backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `rest_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_file`
--

DROP TABLE IF EXISTS `rest_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type_file` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `backup_id` int(11) NOT NULL,
  `file_system_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rest_file_backup_id_859543d6_fk_rest_backup_id` (`backup_id`),
  KEY `rest_file_file_system_id_51dc76e0_fk_rest_filesys_id` (`file_system_id`),
  CONSTRAINT `rest_file_backup_id_859543d6_fk_rest_backup_id` FOREIGN KEY (`backup_id`) REFERENCES `rest_backup` (`id`),
  CONSTRAINT `rest_file_file_system_id_51dc76e0_fk_rest_filesys_id` FOREIGN KEY (`file_system_id`) REFERENCES `rest_filesys` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=253 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_file`
--

LOCK TABLES `rest_file` WRITE;
/*!40000 ALTER TABLE `rest_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `rest_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_filedata`
--

DROP TABLE IF EXISTS `rest_filedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_filedata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `block_id` int(11) NOT NULL,
  `checksum` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_data` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rest_filedata_file_object_id_e92f5099_fk_rest_file_id` (`file_object_id`),
  CONSTRAINT `rest_filedata_file_object_id_e92f5099_fk_rest_file_id` FOREIGN KEY (`file_object_id`) REFERENCES `rest_file` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=526 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_filedata`
--

LOCK TABLES `rest_filedata` WRITE;
/*!40000 ALTER TABLE `rest_filedata` DISABLE KEYS */;
/*!40000 ALTER TABLE `rest_filedata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_filesys`
--

DROP TABLE IF EXISTS `rest_filesys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_filesys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_system` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_filesys`
--

LOCK TABLES `rest_filesys` WRITE;
/*!40000 ALTER TABLE `rest_filesys` DISABLE KEYS */;
INSERT INTO `rest_filesys` VALUES (1,'ext4');
/*!40000 ALTER TABLE `rest_filesys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_keyuser`
--

DROP TABLE IF EXISTS `rest_keyuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_keyuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(44) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `rest_keyuser_user_id_adc7a200_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_keyuser`
--

LOCK TABLES `rest_keyuser` WRITE;
/*!40000 ALTER TABLE `rest_keyuser` DISABLE KEYS */;
INSERT INTO `rest_keyuser` VALUES (1,'WoNiutv5X3Cg3vAvTlRCSV21_KJ3xK184SEtmHlYLCM=',1);
/*!40000 ALTER TABLE `rest_keyuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-24 10:40:30
