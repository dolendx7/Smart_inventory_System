# Smart Inventory System

A web-based inventory management system built with Flask and MySQL. Designed for small to medium businesses to manage products, suppliers, buyers, sales, and stock levels from a single dashboard.

## Features

- User authentication (signup/login)
- Product management with stock tracking
- Supplier and buyer management
- Sales recording with itemized orders
- Low stock alerts and reorder level monitoring
- Financial and inventory reports
- Dashboard with charts and key metrics

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript

## Requirements

- Python 3.8+
- MySQL Server

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/dolendx7/Smart_inventory_System.git
cd Smart_inventory_System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up the database**

Import the schema into MySQL:
```bash
mysql -u root -p < database/schema.sql
```

**4. Configure database credentials**

In `app.py`, update the database config:
```python
DB_HOST = 'localhost'
DB_USER = 'your_mysql_username'
DB_PASSWORD = 'your_mysql_password'
```

**5. Run the app**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
Smart_Inventory_System/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── database/
│   └── schema.sql          # MySQL database schema
├── templates/              # HTML templates
└── static/
    ├── css/                # Stylesheets
    └── js/                 # JavaScript files
```

## Notes

- Default port is 5000
- Change `app.secret_key` in `app.py` before deploying to production
