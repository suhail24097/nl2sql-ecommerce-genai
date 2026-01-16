-- =========================
-- Temporary staging table
-- =========================
CREATE TABLE staging_ecommerce (
    customer_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    age_group VARCHAR(20),
    signup_date DATE,
    country VARCHAR(50),
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    quantity INTEGER,
    unit_price NUMERIC,
    order_id VARCHAR(20),
    order_date DATE,
    order_status VARCHAR(20),
    payment_method VARCHAR(50),
    rating INTEGER,
    review_text TEXT,
    review_id VARCHAR(20),
    review_date DATE
);

-- =========================
-- Load CSV data
-- =========================
-- NOTE: Path will be mounted via Docker later
COPY staging_ecommerce
FROM '/data/ecommerce_dataset_10000.csv'
DELIMITER ','
CSV HEADER;

-- =========================
-- Insert Customers
-- =========================
INSERT INTO customers
SELECT DISTINCT
    customer_id,
    first_name,
    last_name,
    gender,
    age_group,
    signup_date,
    country
FROM staging_ecommerce;

-- =========================
-- Insert Products
-- =========================
INSERT INTO products
SELECT DISTINCT
    product_id,
    product_name,
    category,
    unit_price
FROM staging_ecommerce;

-- =========================
-- Insert Orders
-- =========================
INSERT INTO orders
SELECT DISTINCT
    order_id,
    customer_id,
    order_date,
    order_status,
    payment_method
FROM staging_ecommerce;

-- =========================
-- Insert Order Items
-- =========================
INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    unit_price
)
SELECT
    order_id,
    product_id,
    quantity,
    unit_price
FROM staging_ecommerce;

-- =========================
-- Insert Reviews
-- =========================
INSERT INTO reviews
SELECT DISTINCT
    review_id,
    customer_id,
    product_id,
    rating,
    review_text,
    review_date
FROM staging_ecommerce;

-- =========================
-- Cleanup
-- =========================
DROP TABLE staging_ecommerce;
