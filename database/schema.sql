-- ============================================
-- InvenLogic Pro - Database Schema
-- Multi-Tenant Admin System
-- ============================================

-- Master database for admin accounts
DROP DATABASE IF EXISTS inventory_master;
CREATE DATABASE inventory_master CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventory_master;

-- ============================================
-- TABLE: admins (Master table)
-- ============================================
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: suppliers
-- ============================================
CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_supplier_name (supplier_name)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: buyers
-- ============================================
CREATE TABLE buyers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    buyer_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_buyer_name (buyer_name)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: products
-- ============================================
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 10,
    max_stock_level INT NOT NULL DEFAULT 100,
    supplier_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    UNIQUE KEY unique_sku_per_admin (admin_id, sku),
    INDEX idx_admin_id (admin_id),
    INDEX idx_sku (sku),
    INDEX idx_product_name (product_name),
    INDEX idx_category (category),
    INDEX idx_stock_quantity (stock_quantity),
    INDEX idx_supplier_id (supplier_id),
    CONSTRAINT chk_unit_price CHECK (unit_price >= 0),
    CONSTRAINT chk_stock_quantity CHECK (stock_quantity >= 0)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: sales
-- ============================================
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    order_number VARCHAR(50) NOT NULL,
    buyer_id INT,
    sale_date DATE NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES buyers(id) ON DELETE SET NULL,
    UNIQUE KEY unique_order_per_admin (admin_id, order_number),
    INDEX idx_admin_id (admin_id),
    INDEX idx_order_number (order_number),
    INDEX idx_sale_date (sale_date),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: sale_items
-- ============================================
CREATE TABLE sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_sale_id (sale_id),
    INDEX idx_product_id (product_id),
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_sale_unit_price CHECK (unit_price >= 0),
    CONSTRAINT chk_subtotal CHECK (subtotal >= 0)
) ENGINE=InnoDB;

-- ============================================
-- TABLE: transactions
-- ============================================
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    product_id INT NOT NULL,
    transaction_type ENUM('ADD', 'UPDATE', 'REMOVE', 'SALE', 'RESTOCK') NOT NULL,
    quantity INT DEFAULT 0,
    notes TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_product_id (product_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_transaction_date (transaction_date)
) ENGINE=InnoDB;

-- ============================================
-- NOTE: Unused database objects removed for optimization
-- Removed: alerts table, 4 views, 2 triggers, 3 stored procedures
-- Reason: Not used by application code (app.py queries tables directly)
-- ============================================

-- ============================================
-- INDEXES FOR OPTIMIZATION
-- ============================================

-- Additional composite indexes for common queries
CREATE INDEX idx_products_category_stock ON products(category, stock_quantity);
CREATE INDEX idx_sales_date_status ON sales(sale_date, status);
CREATE INDEX idx_sale_items_product_sale ON sale_items(product_id, sale_id);
CREATE INDEX idx_transactions_product_date ON transactions(product_id, transaction_date);

-- ============================================
-- DATABASE SETUP COMPLETE
-- ============================================
SELECT 'Database schema created successfully!' AS Status;
SELECT 'Ready for production use' AS Info;