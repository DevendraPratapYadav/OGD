-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2017 at 06:08 PM
-- Server version: 10.1.26-MariaDB
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ogd`
--

-- --------------------------------------------------------

--
-- Table structure for table `riceproduction_statewise_inthousandtonnes`
--

CREATE TABLE `riceproduction_statewise_inthousandtonnes` (
  `Entry` int(11) NOT NULL,
  `State` varchar(256) DEFAULT NULL,
  `Production of Rice: Avg. Production(2010-2014)` double(50,5) DEFAULT NULL,
  `Production of Rice: Avg. Production(2014-2015)` double(50,5) DEFAULT NULL,
  `Production of Rice: Avg. Production(2015-2016)` double(50,5) DEFAULT NULL,
  `Inc(+)/Dec(-) as compared to: Avg. Production(2010-2014)` double(50,5) DEFAULT NULL,
  `Inc(+)/Dec(-) as compared to: 2014-15` double(50,5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='[-1 1 0 0 0 0 0]';

--
-- Dumping data for table `riceproduction_statewise_inthousandtonnes`
--

INSERT INTO `riceproduction_statewise_inthousandtonnes` (`Entry`, `State`, `Production of Rice: Avg. Production(2010-2014)`, `Production of Rice: Avg. Production(2014-2015)`, `Production of Rice: Avg. Production(2015-2016)`, `Inc(+)/Dec(-) as compared to: Avg. Production(2010-2014)`, `Inc(+)/Dec(-) as compared to: 2014-15`) VALUES
(1, 'Andhra Pradesh', 7338.90000, 7233.90000, 6940.00000, -398.90000, -293.90000),
(2, 'Assam', 4906.20000, 5222.60000, 5123.00000, 216.80000, -99.60000),
(3, 'Bihar', 5931.30000, 6356.70000, 6106.30000, 175.00000, -250.40000),
(4, 'Chhattisgarh', 6366.90000, 6322.10000, 6294.70000, -72.20000, -27.40000),
(5, 'Gujarat', 1658.90000, 1830.90000, 1564.00000, -94.90000, -266.90000),
(6, 'Haryana', 3842.20000, 4006.00000, 4176.20000, 334.00000, 170.20000),
(7, 'Himachal Pradesh', 126.40000, 125.20000, 98.60000, -27.80000, -26.60000),
(8, 'Jammu & Kashmir', 599.70000, 517.20000, 416.10000, -183.60000, -101.10000),
(9, 'Jharkhand', 2715.60000, 3361.90000, 3456.40000, 740.80000, 94.60000),
(10, 'Karnataka', 3724.10000, 3541.00000, 3393.00000, -331.10000, -148.00000),
(11, 'Kerala', 534.30000, 562.10000, 697.30000, 163.00000, 135.20000),
(12, 'Madhya Pradesh', 2648.90000, 3625.30000, 3487.30000, 838.40000, -138.00000),
(13, 'Maharashtra', 2932.00000, 2946.00000, 2614.00000, -318.00000, -332.00000),
(14, 'Orissa', 7168.40000, 8298.20000, 5795.10000, -1373.30000, -2503.10000),
(15, 'Punjab', 11025.40000, 11107.00000, 11637.00000, 611.60000, 530.00000),
(16, 'Rajasthan', 284.10000, 366.70000, 353.70000, 69.60000, -12.90000),
(17, 'Tamilnadu', 5675.70000, 5727.80000, 5716.70000, 41.00000, -11.10000),
(18, 'Telengana', 5305.50000, 4440.80000, 4194.90000, -1110.60000, -245.90000),
(19, 'Uttar Pradesh', 13446.80000, 12167.90000, 12509.00000, -937.80000, 341.10000),
(20, 'Uttarakhand', 581.30000, 603.70000, 630.00000, 48.70000, 26.30000),
(21, 'West Bengal', 14544.70000, 14677.20000, 16100.00000, 1555.30000, 1422.80000),
(22, 'Others', 2370.60000, 2441.70000, 2309.30000, -61.30000, -132.40000),
(23, 'All', 103728.00000, 105482.10000, 103612.70000, -115.30000, -1869.30000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `riceproduction_statewise_inthousandtonnes`
--
ALTER TABLE `riceproduction_statewise_inthousandtonnes`
  ADD PRIMARY KEY (`Entry`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `riceproduction_statewise_inthousandtonnes`
--
ALTER TABLE `riceproduction_statewise_inthousandtonnes`
  MODIFY `Entry` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
