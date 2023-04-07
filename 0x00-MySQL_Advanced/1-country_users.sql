-- creating a table of users consisting of the following columns:
-- id, integer, never null
-- country, enumeration of countries: US, CO and TN, never null (default = US)
-- email, string (255)
-- name, string (255)

CREATE TABLE IF NOT EXISTS users (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
name VARCHAR(255),
country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);