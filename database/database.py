import mysql.connector
from mysql.connector import Error


def setup_database():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="atoui")

        if conn.is_connected():
            cursor = conn.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS `management`;")
            print("✔ Database 'management' checked/created successfully.")

            cursor.execute("USE `management`;")

            cursor.execute("DROP TABLE IF EXISTS `room`;")
            print("✔ Old 'room' table dropped (if it existed) to apply new updates.")

            users_table = """
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `username` VARCHAR(100) NOT NULL UNIQUE,
                `email` VARCHAR(150) NOT NULL UNIQUE,
                `password` VARCHAR(255) NOT NULL,
                PRIMARY KEY (`id`)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
            """
            cursor.execute(users_table)
            print("✔ Table 'users' checked/created successfully.")

            customer_table = """
            CREATE TABLE IF NOT EXISTS `customer` (
                `Ref` INT NOT NULL,
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
            """
            cursor.execute(customer_table)
            print("✔ Table 'customer' checked/created successfully.")

            room_table = """
            CREATE TABLE IF NOT EXISTS `room` (
                `booking_id` INT NOT NULL AUTO_INCREMENT,
                `Contact` VARCHAR(20) NOT NULL,
                `Check_in` VARCHAR(50) NOT NULL,
                `Check_out` VARCHAR(50) NOT NULL,
                `Room_type` VARCHAR(50) NOT NULL,
                `Room_available` VARCHAR(50) NOT NULL,
                `Meal` VARCHAR(50) NOT NULL,
                `No_of_days` INT NOT NULL,
                `Total_price` DECIMAL(10, 2) DEFAULT 0.00,
                PRIMARY KEY (`booking_id`)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
            """
            cursor.execute(room_table)
            print("✔ Table 'room' (Updated Version) created successfully.")

            conn.commit()
            print("\n🎉 All configurations applied to MySQL successfully!")

    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")

    finally:
        if "conn" in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔒 MySQL connection is closed.")


if __name__ == "__main__":
    setup_database()
