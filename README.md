# Smart Inventory System (InvenLogic Pro)

[![Live Demo](https://img.shields.io/badge/Vercel-Live_Demo-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://smart-inventory-system-dolendx7.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com)

🌐 **Live Deployment URL:** [https://smart-inventory-system-dolendx7.vercel.app](https://smart-inventory-system-dolendx7.vercel.app)

A full-featured web-based inventory management system built with Flask and MySQL. Designed for modern businesses to manage products, suppliers, buyers, sales, transactions, and real-time stock levels from a unified dashboard.

---

## Features

- **User Authentication:** Secure admin signup, login, session management, and password hashing (SHA-256).
- **Product Management:** Complete CRUD with SKU tracking, category filtering, unit prices, and auto reorder levels.
- **Supplier & Buyer Directory:** Contact details, order history, and relationship tracking.
- **Sales & Orders:** Multi-item sales recording, payment statuses (Paid/Unpaid/Partial), and methods (UPI, Card, Cash).
- **Inventory Analytics:** Real-time stock alerts, low-stock notifications, transaction logs, and financial metrics.
- **Responsive Dashboard:** Interactive charts, quick actions, and data tables.

---

## Tech Stack

- **Backend:** Python, Flask, Werkzeug
- **Database:** MySQL (Local or Cloud Serverless)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Deployment:** Vercel (Serverless Functions via `api/index.py`)

---

## Deploying to Vercel

This repository is pre-configured for automated serverless deployment on [Vercel](https://vercel.com):

1. **Import Project into Vercel:**
   - Link your GitHub repository `dolendx7/Smart_inventory_System`.
   - Vercel automatically detects `vercel.json` and Python functions in `api/`.

2. **Domain / URL Configuration:**
   - In **Project Settings** > **Domains**, assign:
     ```
     smart-inventory-system-dolendx7.vercel.app
     ```
     *(or `smart-inventory-system.vercel.app` if available)*.

3. **Configure Environment Variables in Vercel:**
   Because Vercel serverless runs in the cloud, connect it to a free cloud MySQL database (e.g. [TiDB Cloud](https://tidbcloud.com/), [Aiven](https://aiven.io/), or [Railway](https://railway.app/)):

   | Variable | Description | Example |
   | :--- | :--- | :--- |
   | `DB_HOST` | Cloud MySQL Host | `gateway01.us-east-1.prod.aws.tidbcloud.com` |
   | `DB_PORT` | MySQL Port | `4000` (or `3306`) |
   | `DB_USER` | MySQL Username | `your_user` |
   | `DB_PASSWORD` | MySQL Password | `your_password` |
   | `DB_NAME` | Database Name | `inventory_master` |
   | `SECRET_KEY` | Flask Session Key | `your-random-secret-key` |

4. **Import Database Schema:**
   Run the SQL statements from [`database/schema.sql`](database/schema.sql) into your cloud MySQL database instance.

---

## Running Locally

### Quick Start (Windows)
Simply double-click **`run.bat`** (or execute `.\run.ps1` in PowerShell). It automatically checks MySQL, activates the virtual environment, and starts the server.

### Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dolendx7/Smart_inventory_System.git
   cd Smart_inventory_System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL Database:**
   Import the schema into your local MySQL server:
   ```bash
   mysql -u root -p < database/schema.sql
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5001](http://127.0.0.1:5001) in your browser.

---

## Project Structure

```
Smart_Inventory_System/
├── api/
│   └── index.py            # Vercel serverless entrypoint
├── database/
│   └── schema.sql          # MySQL database schema & tables
├── static/
│   ├── css/                # Stylesheets
│   └── js/                 # Client scripts & chart logic
├── templates/              # HTML templates
├── app.py                  # Core Flask application & routes
├── vercel.json             # Vercel deployment & rewrite configuration
├── run.bat                 # 1-click Windows launcher
├── run.ps1                 # PowerShell startup script
├── requirements.txt        # Python dependencies
└── README.md
```

---

## GitHub Repository Setup

To display the live link in the **About** section on GitHub:
1. Go to your repository on GitHub: `https://github.com/dolendx7/Smart_inventory_System`
2. In the right-hand sidebar, click the **⚙️ (gear icon)** next to **About**.
3. In the **Website** field, enter:
   ```
   https://smart-inventory-system-dolendx7.vercel.app
   ```
4. Check **Use your README**, add topics like `flask`, `mysql`, `inventory-management`, `vercel`, and click **Save changes**.
