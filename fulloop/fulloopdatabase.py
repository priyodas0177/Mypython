
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'Admin',
    is_active TINYINT(1) DEFAULT 1
);

-- Insert a default admin
INSERT INTO admin (name, password, role, is_active)
VALUES ('superadmin', 'admin123', 'Admin', 1);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    gender VARCHAR(10),
    role VARCHAR(50),
    is_active TINYINT(1) DEFAULT 1
);