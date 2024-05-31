CREATE DATABASE IF NOT EXISTS remine000db;
USE remine000db;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATETIME,
    status VARCHAR(50)
);