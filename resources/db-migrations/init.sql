
DROP TABLE IF EXISTS favorite_item;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone INT(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE favorite_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);



INSERT INTO items (name, price, stock)
VALUES
    ('Pure Joy', 24.99, 35),
    ('Happiness Burst', 22.49, 45),
    ('Sadness', 5.99, 200),
    ('Deep Sadness', 6.99, 180),
    ('Bittersweet Nostalgia', 13.99, 70),
    ('Mild  Anger', 8.49, 140),
    ('Quiet Serenity', 51.99, 18),
    ('Love', 99.99, 10),
    ('Burning Love', 109.99, 8),
    ('Mild Curiosity', 12.99, 75),
    ('Overwhelming Fear', 4.49, 90),
    ('Eternal Hope', 34.99, 25),
    ('Subtle Joy', 19.49, 55),
    ('Gentle Sadness', 5.49, 210),
    ('Fiery Anger', 9.49, 130),
    ('Calm Hope', 31.99, 30),
    ('Joyful Anticipation', 28.99, 40),
    ('Melancholy', 11.99, 80),
    ('Desperation', 13.49, 55),
    ('Serene Peace', 48.99, 22),
    ('Euphoric Bliss', 37.99, 15),
    ('Mourning', 6.49, 140),
    ('Lustful Desire', 69.99, 10),
    ('Hopeful Optimism', 33.99, 30),
    ('Confusion', 4.99, 150),
    ('Shame', 8.99, 100),
    ('Panic', 7.49, 130),
    ('Indifference', 2.99, 200),
    ('Excited Curiosity', 19.99, 50),
    ('Guilt', 5.49, 180),
    ('Longing', 12.49, 70),
    ('Frustration', 6.29, 160),
    ('Nostalgic Bliss', 15.99, 50),
    ('Regret', 7.99, 140);

 CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    shipping_address VARCHAR(255) NOT NULL,
    total_price DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(10) NOT NULL DEFAULT 'TEMP',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id)
);