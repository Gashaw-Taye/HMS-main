-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 24, 2022 at 05:23 AM
-- Server version: 10.6.4-MariaDB-log
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bernos`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `appointed_by` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `appt_date` varchar(16) NOT NULL,
  `description` varchar(150) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `appointed_by`, `patient_id`, `appt_date`, `description`, `created_at`, `updated_at`, `status`) VALUES
(9, 1, 11, '2022-08-25 05:00', 'Test organisation hello', 1660836526, 1660975406, 1),
(10, 1, 11, '2022-08-19 05:30', 'Test organisation', 1660975766, 1660975766, 1),
(11, 1, 11, '2022-08-19 05:30', 'Test organisation', 1660975988, 1660975988, 1),
(12, 1, 11, '2022-08-19 05:30', 'Test organisation', 1660976006, 1660976006, 1),
(13, 1, 3, '2022-08-19 05:30', 'Test organisation', 1660987068, 1660987068, 1);

-- --------------------------------------------------------

--
-- Table structure for table `bed_rooms`
--

CREATE TABLE `bed_rooms` (
  `id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `bed_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bed_rooms`
--

INSERT INTO `bed_rooms` (`id`, `room_id`, `bed_name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'B1001', 'Room 1 Bed room 1 ', 1, NULL, NULL),
(2, 1, 'R1002', 'Room 1 bed 2', 1, NULL, NULL),
(3, 1, 'B002', 'This is building one for test', 1, 1660976499, 1660976499);

-- --------------------------------------------------------

--
-- Table structure for table `building`
--

CREATE TABLE `building` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `building`
--

INSERT INTO `building` (`id`, `name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Test', 'Information? <>!#%%Technology!%%#^&%* & Telecom', 0, 1635446239, 1635446545),
(2, 'B002', 'This is building one for admin office', 1, 1635446345, 1635446494);

-- --------------------------------------------------------

--
-- Table structure for table `buildings`
--

CREATE TABLE `buildings` (
  `id` int(11) NOT NULL,
  `org_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 1,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `buildings`
--

INSERT INTO `buildings` (`id`, `org_id`, `name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'B001', 'building 1', 0, NULL, 1661101508),
(2, 1, 'B002', 'This is building one for admin office xx', 0, 1660771937, 1661101668),
(3, 1, 'B002', 'This is building one for test', 1, 1661101504, 1661101504);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `description` text NOT NULL,
  `created` datetime NOT NULL,
  `modified` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`, `created`, `modified`) VALUES
(1, 'Fashion', 'Category for anything related to fashion.', '2014-06-01 00:35:07', '2014-05-30 14:34:33'),
(2, 'Electronics', 'Gadgets, drones and more.', '2014-06-01 00:35:07', '2014-05-30 14:34:33'),
(3, 'Motors', 'Motor sports and more', '2014-06-01 00:35:07', '2014-05-30 14:34:54'),
(5, 'Movies', 'Movie products.', '0000-00-00 00:00:00', '2016-01-08 10:27:26'),
(6, 'Books', 'Kindle books, audio books and more.', '0000-00-00 00:00:00', '2016-01-08 10:27:47'),
(13, 'Sports', 'Drop into new winter gear.', '2016-01-09 02:24:24', '2016-01-08 22:24:24');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` int(11) NOT NULL,
  `report_to` int(11) DEFAULT NULL,
  `org_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`id`, `report_to`, `org_id`, `name`, `status`, `created_at`, `updated_at`) VALUES
(1, NULL, 1, 'Pediatrics', 0, 1660768227, 1661102220),
(2, NULL, 1, 'Gynecology', 1, 1660768227, 1660768227),
(3, NULL, 1, 'test', 1, 1661102284, 1661102284);

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `grand_father` varchar(50) DEFAULT NULL,
  `gender` varchar(5) NOT NULL,
  `date_of_birth` varchar(20) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `person_type` varchar(20) NOT NULL,
  `prefix` varchar(10) DEFAULT NULL,
  `profile_image` varchar(200) DEFAULT NULL,
  `org_id` int(11) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`id`, `first_name`, `last_name`, `grand_father`, `gender`, `date_of_birth`, `email`, `person_type`, `prefix`, `profile_image`, `org_id`, `created_at`, `updated_at`, `status`) VALUES
(1, 'Direselign', 'Addis', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'nurse', 'ato', 'test.png', 1, 1660770161, 1660976780, 1),
(2, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660976765, 1660976765, 1),
(3, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660991615, 1660991615, 1),
(4, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660991703, 1660991703, 1),
(5, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660993443, 1660993443, 1);

-- --------------------------------------------------------

--
-- Table structure for table `labs`
--

CREATE TABLE `labs` (
  `id` int(11) NOT NULL,
  `lab_group_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `labs`
--

INSERT INTO `labs` (`id`, `lab_group_id`, `name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'Blood Films', 'Bllod Film', 1, 1638094164, 1638094462),
(2, 1, 'CBC', 'CBC', 0, 1638094490, 1638094518),
(3, 1, 'Blood Filmx', 'Bllod Film', 1, 1660741998, 1660741998),
(4, 2, 'Blood Filmx', 'Bllod Film', 1, 1660749887, 1660749887),
(5, 5, 'Blood Filmx', 'Bllod Film', 1, 1660749933, 1660749933),
(6, 5, 'Blood Filmx', 'Bllod Film', 1, 1661101292, 1661101292);

-- --------------------------------------------------------

--
-- Table structure for table `lab_group`
--

CREATE TABLE `lab_group` (
  `id` int(11) NOT NULL,
  `org_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `lab_group`
--

INSERT INTO `lab_group` (`id`, `org_id`, `name`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'Blood Chemistry Lab', 1, 1638093338, 1660976946),
(2, 1, 'Stool Lab', 1, 1638093373, 1638093373),
(3, 1, 'X-Ray', 1, 1638093383, 1638093383),
(4, 1, 'Radiology', 0, 1638093392, 1638093482),
(5, 1, 'X-ray', 1, 1660749919, 1660749919),
(6, 1, 'X-ray', 1, 1660976937, 1660976937);

-- --------------------------------------------------------

--
-- Table structure for table `lab_requests`
--

CREATE TABLE `lab_requests` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `requested_by` int(11) NOT NULL,
  `lab_expert` int(11) DEFAULT NULL,
  `lab_id` int(11) NOT NULL,
  `lab_result` varchar(255) DEFAULT NULL,
  `lab_result_attachment` varchar(255) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `lab_requests`
--

INSERT INTO `lab_requests` (`id`, `patient_id`, `requested_by`, `lab_expert`, `lab_id`, `lab_result`, `lab_result_attachment`, `status`, `created_at`, `updated_at`) VALUES
(1, 5, 1, 3, 1, 'retest lab data', '', 0, 1660739695, 1660740702),
(2, 5, 1, 3, 1, 'test 2 lab data', '', 1, 1660740058, 1660740058),
(3, 5, 1, 3, 1, 'test 2 lab data', '', 1, 1660740917, 1660740917),
(4, 5, 1, 3, 1, 'test 2 lab data', '', 1, 1660741134, 1660741134),
(5, 5, 1, 3, 1, 'test 2 lab data', '', 1, 1660741210, 1660741210),
(6, 12, 1, 3, 1, 'This is the status', '', 2, 1660802529, 1660802721),
(7, 3, 1, 3, 1, 'This is the status ddfgfg', '', 2, 1660806022, 1660977928),
(8, 3, 1, 3, 1, 'test 2 lab data', '', 0, 1660806138, 1660806149),
(9, 3, 1, 3, 1, 'test 2 lab data', NULL, 1, 1660977238, 1660977238);

-- --------------------------------------------------------

--
-- Table structure for table `office`
--

CREATE TABLE `office` (
  `id` int(11) NOT NULL,
  `main_branch` int(11) DEFAULT NULL,
  `off_name` varchar(50) NOT NULL,
  `off_description` varchar(50) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `office`
--

INSERT INTO `office` (`id`, `main_branch`, `off_name`, `off_description`, `created_at`, `updated_at`, `status`) VALUES
(1, 1, 'DMUx', 'Debre Markos university', 1635593824, 1661102956, 0),
(3, NULL, 'DMU', 'Debre Markos university', 1635593922, 1635593922, 1),
(4, 1, 'DMUx', 'Debre Markos university', 1661102936, 1661102936, 1);

-- --------------------------------------------------------

--
-- Table structure for table `office_expenses`
--

CREATE TABLE `office_expenses` (
  `id` int(11) NOT NULL,
  `reason` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `paid_by` varchar(50) NOT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `office_expenses`
--

INSERT INTO `office_expenses` (`id`, `reason`, `price`, `paid_by`, `status`, `created_at`, `updated_at`) VALUES
(1, 'water', 75, 'abebe', 1, 1639382203, 1639382203);

-- --------------------------------------------------------

--
-- Table structure for table `ope_history`
--

CREATE TABLE `ope_history` (
  `id` int(11) NOT NULL,
  `ope_userid` varchar(50) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `ope_type` varchar(100) NOT NULL,
  `ope_before` varchar(100) NOT NULL,
  `ope_after` varchar(100) NOT NULL,
  `ope_on` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

CREATE TABLE `organization` (
  `id` int(11) NOT NULL,
  `org_name` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `organization`
--

INSERT INTO `organization` (`id`, `org_name`, `status`, `created_at`, `updated_at`) VALUES
(1, 'bete Markos', 1, 1635395646, 1635395646),
(2, 'Habtamu Higher Markosx', 0, 1635395805, 1661103408),
(7, 'My Test org', 0, 1660771205, 1661103364),
(8, 'Test organisation ffgfgh', 1, 1661103343, 1661103343);

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `consulted_by` int(11) DEFAULT NULL,
  `pre_examination` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `examinations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `patient_id`, `consulted_by`, `pre_examination`, `examinations`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 2, '{\"test\":\"test\"}', '{\"hello\":\"dfdf\"}', 1, 123456, 123456),
(2, 5, 4, '{\"blood\":\"23\"}', '{\"test\":\"ddd\"}', 2, 1641998029, 1641998029),
(4, 6, 1, '{\"testing\":123}', '{\"hello\":34}', 2, 123456, 123456),
(5, 6, 1, '{\"testing\":123}', '{\"hello\":34}', 2, 123456, 123456),
(6, 1, 2, 'temp:27, weight:78', '', 1, 1643458905, 1643458905),
(7, 1, 2, 'temp:27, weight:78', '', 1, 1643458931, 1643458931),
(8, 11, 2, 'temp:27, weight:78', '', 1, 1660773450, 1660773450),
(9, 12, 2, 'temp:27, weight:78, dsfsdf:345, dfgdfg:dfgdfg', '', 1, 1660773650, 1660802398),
(10, 12, 2, 'temp:27, weight:80', '', 0, 1660802420, 1660802467),
(11, 3, 2, 'temp:27, weight:78', NULL, 1, 1660986493, 1660986493);

-- --------------------------------------------------------

--
-- Table structure for table `patient_room`
--

CREATE TABLE `patient_room` (
  `id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `enterance_date` int(11) NOT NULL,
  `leave_date` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patient_room`
--

INSERT INTO `patient_room` (`id`, `person_id`, `room_id`, `enterance_date`, `leave_date`, `status`, `created_at`, `updated_at`) VALUES
(1, 5, 1, 164199717, NULL, 1, 164199717, 164199717),
(2, 6, 2, 1635446345, NULL, 1, 1635446345, 1635446345);

-- --------------------------------------------------------

--
-- Table structure for table `persons`
--

CREATE TABLE `persons` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `grand_father` varchar(50) DEFAULT NULL,
  `gender` varchar(5) NOT NULL,
  `date_of_birth` varchar(20) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `person_type` varchar(20) NOT NULL,
  `prefix` varchar(10) DEFAULT NULL,
  `profile_image` varchar(200) DEFAULT NULL,
  `org_id` int(11) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `persons`
--

INSERT INTO `persons` (`id`, `first_name`, `last_name`, `grand_father`, `gender`, `date_of_birth`, `email`, `person_type`, `prefix`, `profile_image`, `org_id`, `created_at`, `updated_at`, `status`) VALUES
(1, 'Abebe', 'Tedila', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'doctor', 'ato', 'test.png', 1, 1638095596, 1638095596, 1),
(2, 'Getachew', 'Balew', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'nurse', 'ato', 'test.png', 1, 1638095632, 1654436206, 2),
(3, 'Muluken', 'Menberu', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'doctor', 'ato', 'test.png', 1, 1641473888, 1641473909, 1),
(4, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1641997101, 1641997101, 5),
(5, 'Patient 1', 'Patient', NULL, 'F', '2011-10-12', 'patient@gmail.com', 'patient', 'w/r', 'test.png', 1, 1641997161, 1641997161, 1),
(6, 'Patient 2', 'Patient', NULL, 'F', '2011-10-12', 'patient@gmail.com', 'patient', 'w/r', 'test.png', 1, 1641997174, 1641997174, 1),
(7, 'test', 'test', NULL, 'Male', '2021-12-12', 'test@test.com', 'patient', 'ato', 'test.png', 1, 1642330179, 1642330179, 1),
(8, 'muluken', 'Menberu', NULL, 'Male', '23434', 'muler@gmail.com', 'patient', 'ato', 'test.png', 1, 1642838304, 1642838304, 1),
(9, 'Fish', 'Dire', NULL, 'Male', 'sfsdf', 'fish@gmail.com', 'fish', 'ato', 'test.png', 1, 1643482762, 1643482762, 1),
(10, 'Mulukentest', 'Menberutest', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'nurse', 'ato', 'test.png', 1, 1659446098, 1659446266, 3),
(11, 'yy', 'Menberutest', NULL, 'Male', '2011-10-12', 'test@gmail.com', 'patient', 'ato', 'test.png', 1, 1660768165, 1660768227, 0),
(12, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660770095, 1660770095, 1),
(13, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660803563, 1660803563, 1),
(14, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660998954, 1660998954, 1),
(15, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660998960, 1660998960, 1),
(16, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660999063, 1660999063, 1),
(17, 'Abat', 'Tariku', NULL, 'Male', '2011-10-12', 'abat@gmail.com', 'doctor', 'Dr', 'test.png', 1, 1660999097, 1660999097, 1);

-- --------------------------------------------------------

--
-- Table structure for table `pharmacy`
--

CREATE TABLE `pharmacy` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `properties` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `order_price` float DEFAULT NULL,
  `sell_price` float DEFAULT NULL,
  `amount` float NOT NULL,
  `org_id` int(11) NOT NULL,
  `expire_date` varchar(20) NOT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pharmacy`
--

INSERT INTO `pharmacy` (`id`, `name`, `properties`, `order_price`, `sell_price`, `amount`, `org_id`, `expire_date`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Diclos', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 0, 1661100552, 1661100681),
(2, 'Diclo', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 1, 1661171191, 1661171191),
(3, 'Diclo', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 1, 1661285433, 1661285433),
(4, 'testing', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 1, 1661285461, 1661285461),
(5, 'testing sdfdsf', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 1, 1661285637, 1661285637),
(6, 'testing sdfdsf hello', 'ddfg', 20.5, 25, 0, 1, '2023-02-01', 1, 1661285662, 1661285662),
(7, 'Diclo', 'ddfg', 20.5, 25, 2, 1, '2023-02-01', 1, 1661318581, 1661318581);

-- --------------------------------------------------------

--
-- Table structure for table `prescriptions`
--

CREATE TABLE `prescriptions` (
  `id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `prescription` varchar(50) NOT NULL,
  `provided_by` int(11) DEFAULT NULL,
  `approved_pharmacist` int(11) DEFAULT NULL,
  `dosage` varchar(50) NOT NULL,
  `frequancy` varchar(50) NOT NULL,
  `no_of_day` varchar(50) NOT NULL,
  `food_relation` varchar(50) NOT NULL,
  `instruction` varchar(50) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `prescriptions`
--

INSERT INTO `prescriptions` (`id`, `person_id`, `prescription`, `provided_by`, `approved_pharmacist`, `dosage`, `frequancy`, `no_of_day`, `food_relation`, `instruction`, `status`, `created_at`, `updated_at`) VALUES
(1, 5, 'dfjslk dfljks jdlkfjsdlkdf jlksjdf', 1, 4, 'ssdfsdf', 'sdfsd', 'sdf', 'sdf', 'sdf', 1, 123456, 123456),
(2, 2, 'Test prese', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 0, 1660546329, 1660547260),
(3, 2, 'thjdhfkjdfg', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 0, 1660546690, 1660547310),
(4, 2, 'thjdhfkjdfg', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 1, 1660546719, 1660546719),
(5, 2, 'This is another one', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 0, 1660547169, 1660547322),
(6, 3, 'This is another one', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 0, 1660805035, 1660805914),
(7, 3, 'This is another one', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 1, 1660805340, 1660805340),
(8, 3, 'Test prese', 1, 3, 'dkdfkg', 'skdhf', 'dfjjk', 'djgkljdfg', 'ldjlkjdfg', 1, 1660805880, 1660805975);

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `org_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `org_id`, `name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'admin', 'admin role', 1, 1639317278, 1639317278),
(2, 1, 'doctor', 'doctor role', 1, 1639317308, 1639317308),
(3, 1, 'nurse', 'nurse role', 1, 1639317322, 1639317322),
(4, 1, 'nurseddd', 'nurse role', 1, 1661068234, 1661068329),
(5, 1, 'Pediatrics', NULL, 1, 1661102241, 1661102241),
(6, 1, 'test', NULL, 1, 1661102267, 1661102267);

-- --------------------------------------------------------

--
-- Table structure for table `role_users`
--

CREATE TABLE `role_users` (
  `id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` tinyint(4) DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role_users`
--

INSERT INTO `role_users` (`id`, `role_id`, `user_id`, `status`, `created_at`, `updated_at`) VALUES
(10, 1, 4, 0, 1661069321, 1661069343),
(11, 1, 1, 1, 1661073128, 1661073128);

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `bld_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `bld_id`, `name`, `description`, `status`, `created_at`, `updated_at`) VALUES
(1, 2, 'B2R001', 'Room 1', 1, NULL, NULL),
(2, 2, 'B2R002', 'Room 2', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `service_category`
--

CREATE TABLE `service_category` (
  `id` int(11) NOT NULL,
  `office_id` int(11) NOT NULL,
  `cat_name` varchar(50) NOT NULL,
  `cat_description` varchar(50) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `service_category`
--

INSERT INTO `service_category` (`id`, `office_id`, `cat_name`, `cat_description`, `created_at`, `updated_at`, `status`) VALUES
(1, 1, 'dfsdf', 'dlfjlkdjfjsdlkf', 1635596167, 1635596167, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `public_id` int(11) DEFAULT NULL,
  `token` text DEFAULT NULL,
  `first_login` int(11) DEFAULT NULL,
  `last_login` int(11) DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT 1,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `public_id`, `token`, `first_login`, `last_login`, `status`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'sha256$9PHERCuiYqKNu0U6$389f2d4a266299533eeb72cc175bdea7738bcf4f9e2a64eccce00c8fd616bce5', 1234, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2MTA3NDAxOCwianRpIjoiNjQyMGVkZDMtNGQwYy00YTBhLTlmMDYtMzI2OTQ3M2FmZDUzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjYxMDc0MDE4LCJleHAiOjE2NjEwNzQ5MTgsInJvbGUiOiJhZG1pbiIsImluZm8iOnsiaWQiOjEsImZpcnN0X25hbWUiOiJ5eSIsImxhc3RfbmFtZSI6ImpmZmYiLCJncmFuZF9mYXRoZXIiOm51bGwsImdlbmRlciI6Ik1hbGUiLCJkYXRlX29mX2JpcnRoIjoiMjAxMS0xMC0xMiIsImVtYWlsIjoidGVzdEBnbWFpbC5jb20iLCJwZXJzb25fdHlwZSI6Im51cnNlIiwicHJlZml4IjoiYXRvIiwicHJvZmlsZV9pbWFnZSI6InRlc3QucG5nIiwib3JnX2lkIjoxLCJjcmVhdGVkX2F0IjoxNjYwNzcwMTYxLCJ1cGRhdGVkX2F0IjoxNjYwOTc2NzgwLCJzdGF0dXMiOjF9fQ.IuppOa8EMwofjbjz8Izm66bUeM3Qtnn79zVFgtk-kEw', NULL, NULL, 1, 1661072997, 1661072997),
(4, 'abebe', 'sha256$PNYKoskyvhHTHDnK$622590165ff464026ffa36748c77e02bd7ecd92350f5251c0f932fa40e8c2827', 1234, NULL, NULL, NULL, 1, 1661013827, 1661013827),
(5, 'abat', 'sha256$ttCsIYmfZW2tnUF0$054f18bce1682e17ce8c5aa93fd7679ca53e2c7340ade4df25b0ec78d3c1da52', 1234, NULL, NULL, NULL, 1, 1661013732, 1661013732);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bed_rooms`
--
ALTER TABLE `bed_rooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `building`
--
ALTER TABLE `building`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `buildings`
--
ALTER TABLE `buildings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `report_to` (`report_to`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `labs`
--
ALTER TABLE `labs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lab_group_id` (`lab_group_id`);

--
-- Indexes for table `lab_group`
--
ALTER TABLE `lab_group`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `lab_requests`
--
ALTER TABLE `lab_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `lab_id` (`lab_id`),
  ADD KEY `requested_by` (`requested_by`),
  ADD KEY `lab_expert` (`lab_expert`);

--
-- Indexes for table `office`
--
ALTER TABLE `office`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_branch` (`main_branch`);

--
-- Indexes for table `office_expenses`
--
ALTER TABLE `office_expenses`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ope_history`
--
ALTER TABLE `ope_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `organization`
--
ALTER TABLE `organization`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `consulted_by` (`consulted_by`);

--
-- Indexes for table `patient_room`
--
ALTER TABLE `patient_room`
  ADD PRIMARY KEY (`id`),
  ADD KEY `person_id` (`person_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `persons`
--
ALTER TABLE `persons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `pharmacy`
--
ALTER TABLE `pharmacy`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `person_id` (`person_id`),
  ADD KEY `provided_by` (`provided_by`),
  ADD KEY `approved_pharmacist` (`approved_pharmacist`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `role_users`
--
ALTER TABLE `role_users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role_id` (`role_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bld_id` (`bld_id`);

--
-- Indexes for table `service_category`
--
ALTER TABLE `service_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `office_id` (`office_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `bed_rooms`
--
ALTER TABLE `bed_rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `building`
--
ALTER TABLE `building`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `buildings`
--
ALTER TABLE `buildings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `labs`
--
ALTER TABLE `labs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `lab_group`
--
ALTER TABLE `lab_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `lab_requests`
--
ALTER TABLE `lab_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `office`
--
ALTER TABLE `office`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `office_expenses`
--
ALTER TABLE `office_expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ope_history`
--
ALTER TABLE `ope_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `organization`
--
ALTER TABLE `organization`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `patient_room`
--
ALTER TABLE `patient_room`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `persons`
--
ALTER TABLE `persons`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `pharmacy`
--
ALTER TABLE `pharmacy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `prescriptions`
--
ALTER TABLE `prescriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `role_users`
--
ALTER TABLE `role_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `service_category`
--
ALTER TABLE `service_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bed_rooms`
--
ALTER TABLE `bed_rooms`
  ADD CONSTRAINT `bed_rooms_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Constraints for table `buildings`
--
ALTER TABLE `buildings`
  ADD CONSTRAINT `buildings_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `departments`
--
ALTER TABLE `departments`
  ADD CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`report_to`) REFERENCES `departments` (`id`),
  ADD CONSTRAINT `departments_ibfk_2` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `labs`
--
ALTER TABLE `labs`
  ADD CONSTRAINT `labs_ibfk_1` FOREIGN KEY (`lab_group_id`) REFERENCES `lab_group` (`id`);

--
-- Constraints for table `lab_group`
--
ALTER TABLE `lab_group`
  ADD CONSTRAINT `lab_group_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `lab_requests`
--
ALTER TABLE `lab_requests`
  ADD CONSTRAINT `lab_requests_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `lab_requests_ibfk_2` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`id`),
  ADD CONSTRAINT `lab_requests_ibfk_3` FOREIGN KEY (`requested_by`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `lab_requests_ibfk_4` FOREIGN KEY (`lab_expert`) REFERENCES `persons` (`id`);

--
-- Constraints for table `office`
--
ALTER TABLE `office`
  ADD CONSTRAINT `office_ibfk_1` FOREIGN KEY (`main_branch`) REFERENCES `office` (`id`);

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `patients_ibfk_2` FOREIGN KEY (`consulted_by`) REFERENCES `persons` (`id`);

--
-- Constraints for table `patient_room`
--
ALTER TABLE `patient_room`
  ADD CONSTRAINT `patient_room_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `patient_room_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

--
-- Constraints for table `persons`
--
ALTER TABLE `persons`
  ADD CONSTRAINT `persons_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `pharmacy`
--
ALTER TABLE `pharmacy`
  ADD CONSTRAINT `pharmacy_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`provided_by`) REFERENCES `persons` (`id`),
  ADD CONSTRAINT `prescriptions_ibfk_3` FOREIGN KEY (`approved_pharmacist`) REFERENCES `persons` (`id`);

--
-- Constraints for table `roles`
--
ALTER TABLE `roles`
  ADD CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`id`);

--
-- Constraints for table `role_users`
--
ALTER TABLE `role_users`
  ADD CONSTRAINT `role_users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  ADD CONSTRAINT `role_users_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`bld_id`) REFERENCES `building` (`id`);

--
-- Constraints for table `service_category`
--
ALTER TABLE `service_category`
  ADD CONSTRAINT `service_category_ibfk_1` FOREIGN KEY (`office_id`) REFERENCES `office` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id`) REFERENCES `employees` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
