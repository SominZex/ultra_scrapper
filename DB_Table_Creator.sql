CREATE DATABASE IF NOT EXISTS web_scraping_db;

USE web_scraping_db;

CREATE TABLE IF NOT EXISTS websites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    meta_title TEXT,
    meta_description TEXT,
    language VARCHAR(10),
    category VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS social_media_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT,
    platform VARCHAR(50),
    url VARCHAR(255),
    FOREIGN KEY (website_id) REFERENCES websites(id)
);

CREATE TABLE IF NOT EXISTS tech_stack (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT,
    technology VARCHAR(50),
    FOREIGN KEY (website_id) REFERENCES websites(id)
);

CREATE TABLE IF NOT EXISTS payment_gateways (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT,
    gateway VARCHAR(50),
    FOREIGN KEY (website_id) REFERENCES websites(id)
);
