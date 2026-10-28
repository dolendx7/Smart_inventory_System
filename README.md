# 📦 Smart Inventory System

> Inventory management built for modern businesses — simple, scalable, and ready to run.

<p align="center">
  <a href="https://smart-inventory-system-teal.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Vercel-Live%20Demo-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
</p>

<p align="center">
  <strong>Track stock, manage suppliers, monitor sales, and stay ahead of inventory issues.</strong>
</p>

---

## 🌐 Live Demo

- Website: [https://smart-inventory-system-teal.vercel.app](https://smart-inventory-system-teal.vercel.app)

---

## 🌟 Overview

Smart Inventory System is a full-featured web-based inventory and sales management platform designed for modern small and medium businesses. It helps teams manage products, suppliers, buyers, stock movements, and transactions from a single dashboard.

The system is built with Flask and MySQL, and it is designed to be easy to deploy, easy to extend, and practical for everyday business operations.

---

## ✨ Key Features

### 📦 Product Management
- Add, update, and delete products
- Track SKU and category information
- Manage unit price, reorder levels, and stock status
- Filter inventory efficiently

### 🧾 Supplier & Buyer Management
- Maintain a supplier and buyer directory
- Store contact information and business details
- Keep historical records for better purchasing decisions

### 💰 Sales & Transactions
- Record sales with multiple products per transaction
- Track payment methods and payment status
- Manage partial, unpaid, and paid orders
- Maintain transaction history and accountability

### 📊 Inventory Analytics
- Monitor low-stock items
- View real-time stock health
- Analyze product movement and financial metrics
- Get alerts when inventory needs attention

### 🧠 Business Dashboard
- Quick overview of inventory and sales performance
- Interactive charts and data summaries
- Clean and responsive UI for daily operations

---

## 🧰 Tech Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, Flask, Werkzeug |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript |
| Deployment | Vercel Serverless Functions |
| Session Security | Flask session handling + password hashing |

---

## 🏗️ Project Structure

```text
Smart_inventory_System/
├── api/                          # Vercel serverless API entry points
├── database/
│   └── schema.sql                # MySQL database schema
├── static/
│   ├── css/                     # Frontend styling
│   └── js/                      # Client-side logic and charts
├── templates/                   # HTML templates
├── app.py                       # Flask application
├── requirements.txt             # Python dependencies
├── run.bat                      # Windows launcher
├── run.ps1                      # PowerShell launcher
├── vercel.json                  # Vercel configuration
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🚀 Local Development Setup

### 1) Clone the repository

```bash
git clone https://github.com/dolendx7/Smart_inventory_System.git
cd Smart_inventory_System
```

### 2) Create a virtual environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Set up the MySQL database

Import the schema:

```bash
mysql -u root -p < database/schema.sql
```

### 5) Run the app

```bash
python app.py
```

Then open:

- `http://127.0.0.1:5001`

---

## ☁️ Deployment on Vercel

This project is prepared for Vercel deployment using serverless Python functions.

### Deployment steps

1. Import the GitHub repository into Vercel.
2. Vercel will detect the backend configuration automatically.
3. Add the required environment variables in the Vercel dashboard.
4. Connect the app to a MySQL database hosted on a cloud provider.

### Recommended environment variables

| Variable | Description | Example |
| --- | --- | --- |
| `DB_HOST` | MySQL hostname | `gateway01.us-east-1.prod.aws.tidbcloud.com` |
| `DB_PORT` | MySQL port | `4000` |
| `DB_USER` | MySQL username | `your_user` |
| `DB_PASSWORD` | MySQL password | `your_password` |
| `DB_NAME` | Database name | `inventory_master` |
| `SECRET_KEY` | Flask secret key | `your-random-secret-key` |

---

## 🧪 Quick Start (Windows)

You can launch the app quickly using the included scripts:

```bash
run.bat
```

or in PowerShell:

```powershell
.\run.ps1
```

This helps validate the environment and starts the app automatically.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a pull request

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Maintainer

- GitHub: [@dolendx7](https://github.com/dolendx7)
- Repository: [Smart_inventory_System](https://github.com/dolendx7/Smart_inventory_System)

---

## 📌 Recommended GitHub Repository Description

Use this as your GitHub repo description:

`Smart Inventory Management System for Products, Stock, Sales, and Supplier Tracking`

This version is clean, professional, and easy to understand for visitors.
