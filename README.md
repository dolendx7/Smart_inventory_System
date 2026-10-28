# 📦 Smart Inventory System

<p align="center">
  <a href="https://smart-inventory-system-teal.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Vercel-Live%20Demo-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo" />
  </a>
  <a href="https://github.com/dolendx7/Smart_inventory_System" target="_blank">
    <img src="https://img.shields.io/badge/Status-Production%20Ready-2ea44f?style=for-the-badge" alt="Production Ready" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask 3.0" />
  <img src="https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
</p>

> Smart inventory management for growth-focused businesses — track stock, monitor sales, manage suppliers, and stay ahead of shortages.

<p align="center">
  <strong>Built to help businesses control inventory with less effort and more visibility.</strong>
</p>

---

## 🌐 Live Demo

- Website: [https://smart-inventory-system-teal.vercel.app](https://smart-inventory-system-teal.vercel.app)

---

## ✨ Overview

Smart Inventory System is a complete inventory and sales management platform for businesses that need a clean, practical way to manage stock, purchases, customer transactions, and operational visibility.

It gives teams a central place to:

- manage products and stock levels
- track suppliers and buyers
- record sales and payment status
- monitor low-stock and expiry risks
- understand performance through analytics and dashboards

The system is designed to be lightweight, scalable, and easy to deploy while still handling the day-to-day needs of a real business.

---

## 🚀 Why This Project Matters

Inventory problems often appear as small issues until they turn into missed sales, wasted stock, or operational confusion.

This project solves that by combining:

- real-time product visibility
- clean transaction tracking
- supplier relationship management
- organized reporting and alerts
- a simple interface for daily operations

In short, it helps businesses run smarter with less friction.

---

## 🧩 Core Features

### 📦 Product & Stock Management
- Add, update, and remove products
- Track SKU, category, stock, and pricing
- Set reorder thresholds and stock alerts
- Manage product inventory in a structured way

### 🧾 Supplier & Buyer Directory
- Store supplier and buyer details in one place
- Track business relationships and contact data
- Maintain a record of transactions and interactions

### 💰 Sales & Payment Tracking
- Create sales entries with multiple products
- Support payment status tracking: Paid / Unpaid / Partial
- Record payment methods like UPI, cash, and card
- Maintain transaction history for accountability

### 📊 Inventory Analytics
- Monitor stock health in real time
- Detect low-stock situations early
- View inventory movement and financial insights
- Understand which items require immediate attention

### 🖥️ Dashboard & Visibility
- Clean business dashboard overview
- Data summaries and quick actions
- Responsive layout for daily operational use
- Simple interface built for practical business workflows

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask, Werkzeug |
| Frontend | HTML5, CSS3, JavaScript |
| Database | MySQL |
| Deployment | Vercel Serverless Functions |
| Security | Flask session handling, SHA-256 password hashing |

---

## 🏗️ Architecture Overview

```text
User Browser
    |
    v
Flask Web App
    |
    +--> Routes / Controllers
    |
    +--> Business Logic
    |
    +--> MySQL Database

Product data, supplier records, buyer data, sales transactions,
transaction logs, and stock data are stored in MySQL and served
through the Flask application.
```

---

## 📁 Project Structure

```text
Smart_inventory_System/
├── api/                          # Vercel serverless entry points
├── database/
│   └── schema.sql                # MySQL schema and table definitions
├── static/
│   ├── css/                     # Stylesheets
│   └── js/                      # Chart logic and frontend behavior
├── templates/                   # HTML templates
├── app.py                       # Flask application and routes
├── requirements.txt             # Python dependencies
├── run.bat                      # Windows startup script
├── run.ps1                      # PowerShell startup script
├── vercel.json                  # Vercel deployment config
├── README.md
├── LICENSE
├── .gitignore
└── .env.example                 # Optional environment template
```

---

## 🚀 Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/dolendx7/Smart_inventory_System.git
cd Smart_inventory_System
```

### 2) Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure MySQL

Import the schema into your local MySQL instance:

```bash
mysql -u root -p < database/schema.sql
```

### 5) Run the application

```bash
python app.py
```

Then open:

- `http://127.0.0.1:5001`

---

## ☁️ Deployment on Vercel

This project is configured for Vercel deployment using serverless functions.

### Deployment steps

1. Import the repository into Vercel.
2. Connect the project to your GitHub repo.
3. Add the required environment variables.
4. Connect the app to a hosted MySQL database.
5. Deploy and use the live domain.

### Recommended environment variables

| Variable | Description | Example |
| --- | --- | --- |
| `DB_HOST` | MySQL host | `gateway01.us-east-1.prod.aws.tidbcloud.com` |
| `DB_PORT` | MySQL port | `4000` |
| `DB_USER` | MySQL username | `your_user` |
| `DB_PASSWORD` | MySQL password | `your_password` |
| `DB_NAME` | Database name | `inventory_master` |
| `SECRET_KEY` | Flask secret key | `your-random-secret-key` |

---

## ⚡ Quick Start (Windows)

```bash
run.bat
```

or:

```powershell
.\run.ps1
```

This is the fastest way to boot the application locally.

---

## 📈 Roadmap

- [x] Core inventory management
- [x] Product, buyer, and supplier tracking
- [x] Sales and payment recording
- [x] Low-stock and analytics support
- [ ] Role-based admin access improvements
- [ ] More advanced reporting and export tools
- [ ] Enhanced dashboard filters and analytics
- [ ] Mobile responsive improvements

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a pull request

We appreciate thoughtful improvements, bug fixes, and useful feature additions.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Maintainer

- GitHub: [@dolendx7](https://github.com/dolendx7)
- Repository: [Smart_inventory_System](https://github.com/dolendx7/Smart_inventory_System)

---

## 🏷️ Recommended Repository Description

Use this as your GitHub repository description:

`Smart Inventory Management System for Products, Stock, Sales, and Supplier Tracking`

This is concise, clear, and professional for GitHub visitors.

---

<p align="center">
  <strong>Manage inventory smarter. Reduce confusion. Improve business control.</strong>
</p>
