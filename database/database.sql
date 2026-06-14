-- =========================================================================
-- DATABASE CONFIGURATION FOR HOTEL MANAGEMENT SYSTEM
-- =========================================================================

-- 1. Create the Database if it does not exist
CREATE DATABASE IF NOT EXISTS `management`;

USE `management`;

-- =========================================================================
-- 2. TABLE STRUCTURE FOR: users
-- Holds authentication data for the login and registration system
-- =========================================================================
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL, -- Holds SHA-256 hashed passwords
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- =========================================================================
-- 3. TABLE STRUCTURE FOR: customer
-- Stores information about checked-in guests and references
-- =========================================================================
CREATE TABLE IF NOT EXISTS `customer` (
    `Ref` INT NOT NULL, -- Auto-generated Unique Customer Reference ID
    `Name` VARCHAR(100) NOT NULL,
    `Family` VARCHAR(100) NOT NULL,
    `Gender` VARCHAR(20) NOT NULL,
    `Post` VARCHAR(50) DEFAULT NULL,
    `Mobile` VARCHAR(20) NOT NULL,
    `Email` VARCHAR(150) DEFAULT NULL,
    `Nationality` VARCHAR(50) NOT NULL,
    `IdProof` VARCHAR(50) NOT NULL,
    `IdNumber` VARCHAR(100) NOT NULL,
    `Address` TEXT DEFAULT NULL,
    PRIMARY KEY (`Ref`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- =========================================================================
-- 4. TABLE STRUCTURE FOR: room
-- Handles room booking, financial records, and checking dates
-- =========================================================================
CREATE TABLE IF NOT EXISTS `room` (
    `booking_id` INT NOT NULL AUTO_INCREMENT,
    `Contact` VARCHAR(20) NOT NULL,
    `Check_in` VARCHAR(50) NOT NULL,
    `Check_out` VARCHAR(50) NOT NULL,
    `Room_type` VARCHAR(50) NOT NULL,
    `Room_available` VARCHAR(50) NOT NULL,
    `Meal` VARCHAR(50) NOT NULL,
    `No_of_days` INT NOT NULL,
    `Total_price` DECIMAL(10, 2) DEFAULT 0.00
    PRIMARY KEY (`booking_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- =========================================================================
-- 5. OPTIONAL: INITIAL DUMMY DATA FOR TESTING
-- Default login password hint: (The application hashes inputs using SHA-256)
-- Username: admin | Password: adminpassword
-- =========================================================================
-- INSERT INTO `users` (`username`, `email`, `password`) VALUES
-- ('admin', 'admin@hotel.com', '716f6e7c81d85fb5e74d12bbd63de33b3796d19488a0b064c5770020aa025a74');
