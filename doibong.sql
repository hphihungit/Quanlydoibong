-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.39 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table doibong.formations: ~0 rows (approximately)
INSERT INTO `formations` (`id`, `name`, `position`, `player_name`) VALUES
	(15, '4-4-2', 'ST1', 'anh'),
	(16, '4-4-2', 'ST2', 'kiệt'),
	(17, '4-4-2', 'LM', 'hùng'),
	(18, '4-4-2', 'CM1', 'hải'),
	(19, '4-4-2', 'CM2', 'hoàng'),
	(20, '4-4-2', 'RM', 'huy'),
	(21, '4-4-2', 'LB', 'hưng'),
	(22, '4-4-2', 'CB1', 'đạt'),
	(23, '4-4-2', 'CB2', 'dũng'),
	(24, '4-4-2', 'RB', 'danh'),
	(25, '4-4-2', 'GK', 'quốc');

-- Dumping data for table doibong.matchs: ~4 rows (approximately)
INSERT INTO `matchs` (`id`, `opponent`, `match_time`, `result`, `team_score`, `opponent_score`, `location`, `tournament`) VALUES
	(1, 'arsenal', '2024-05-14 14:29:22', 'Thắng', 5, 0, 'Away', 'EPL'),
	(2, 'hy', '2023-05-14 14:46:58', 'Hòa', 2, 2, 'Old Sanford', 'EPL'),
	(3, 'chelsea', '2025-05-14 14:57:50', 'Thua', 1, 3, 'Old Sanford', 'Champions League'),
	(4, 'arsenal', '2024-05-14 14:29:22', 'Thắng', 7, 2, 'Away', 'EPL'),
	(5, 'haha', '2025-05-14 22:10:41', 'Thắng', 3, 0, 'Old Sanford', 'Giao hữu');

-- Dumping data for table doibong.players: ~11 rows (approximately)
INSERT INTO `players` (`id`, `name`, `birthday`, `position`, `country`, `shirt_number`, `height`, `weight`, `goals`, `assists`) VALUES
	(1, 'anh', '2025-05-14', 'cm', 'viet nam', 1, 12, 12, 35, 12),
	(2, 'kiệt', '2023-05-15', 'rw', 'viet na', 12, 12, 12, 12, 12),
	(4, 'hùng', '2004-05-15', 'lw', 'viet nam', 11, 1212, 12, 32, 14),
	(5, 'hải', '2025-05-14', 'cf', 'viet nam', 10, 189, 85, 30, 20),
	(6, 'hoàng', '2025-05-15', 'cf', 'viet nam', 13, 187, 84, 20, 21),
	(7, 'huy', '2025-05-15', 'cb', 'viet nam', 14, 178, 74, 21, 12),
	(8, 'hưng', '2025-05-14', 'rb', 'viet nam', 22, 174, 72, 12, 23),
	(9, 'đạt', '2025-05-15', 'lb', 'viet nam', 43, 183, 84, 21, 23),
	(10, 'dũng', '2004-05-15', 'cm', 'viet nam', 42, 178, 78, 12, 23),
	(11, 'quốc', '2004-05-15', 'gk', 'viet nam', 23, 194, 94, 2, 2),
	(12, 'danh', '2025-05-14', 'cm', 'viet nam', 12, 178, 67, 23, 32);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
