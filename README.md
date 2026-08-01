# 🚗 DriveBD: Smart Driver & Vehicle Owner Portal

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**DriveBD** is a comprehensive web application designed to simulate the national driver and vehicle management system of Bangladesh. Built with **Python**, **Streamlit**, and **SQLAlchemy**, it provides a centralized platform for vehicle owners, drivers, and administrators to manage registrations, traffic violations, digital documents, vehicle maintenance, and fine payments.

> ⚠️ **Disclaimer:** This is an academic/portfolio capstone project. It is **not affiliated with, endorsed by, or connected to BRTA** (Bangladesh Road Transport Authority), Bangladesh Police, or any government organization. All data, users, and records are synthetically generated for demonstration purposes only.

---

# 📖 Overview

DriveBD is a full-stack simulation of a national digital driver and vehicle management portal inspired by Bangladesh's transportation ecosystem.

The project demonstrates how a modern e-government service could work by combining:

- Secure authentication
- Role-Based Access Control (RBAC)
- Vehicle Registration
- Traffic Violation Management
- Digital Document Vault
- Service History
- Fine Payment System
- Data Analytics
- Mock BRTA APIs
- AI-based Violation Detection Demo

The system is designed for educational, research, and portfolio purposes while following real-world software engineering practices.

---

# ✨ Key Features

## 🔐 Authentication & RBAC

- Secure Login
- Bcrypt Password Hashing
- Session Management
- Three Roles:
  - Admin
  - Vehicle Owner
  - Driver

---

## 📊 Smart Dashboard

Role-based dashboard showing

- Vehicle Count
- Total Violations
- Pending Payments
- Upcoming Expiry Alerts
- Recent Activities
- Quick Navigation Cards

---

## 🚘 Vehicle Management

- Register Vehicle
- Edit Vehicle Information
- Search Vehicles
- Vehicle Ownership
- Registration Status
- Fitness Information

---

## 🚦 Traffic Violation System

- Create Violations
- Automatic Fine Calculation
- Violation Categories
- Payment Status
- Violation History
- Evidence Image Support (Demo)

---

## 💳 Digital Payment Portal

Supported mock payment methods

- bKash
- Nagad
- Debit/Credit Card
- Bank Transfer

Features

- Instant Payment
- Payment History
- Downloadable PDF Receipt
- Status Tracking

---

## 📂 Digital Document Vault

Store and monitor

- National ID
- Driving License
- Vehicle Registration
- Fitness Certificate
- Tax Token
- Insurance

Includes automatic expiry reminders.

---

## 🔧 Vehicle Service History

Maintain

- Oil Changes
- Repairs
- Servicing
- Cost Tracking
- Workshop Details
- Service Timeline

---

## 📝 Appeals Management

Drivers may

- Submit Appeals
- Track Appeal Status
- View Decisions
- Upload Supporting Information

Admins can

- Approve Appeals
- Reject Appeals
- Add Comments

---

## 👨‍💼 Admin Control Panel

Administrator capabilities include

- User Management
- Role Management
- System Logs
- Dashboard Analytics
- Approve Appeals
- Edit Configuration
- Database Overview

---

## 📈 Data Analytics

Interactive Plotly Charts

- Violation Distribution
- Monthly Revenue
- Payment Trends
- Violation Types
- User Statistics
- Outstanding Fine Analysis

---

## 📑 Report Generation

Export

- CSV Reports
- PDF Reports
- Payment Reports
- Violation Reports
- Vehicle Reports

---

## 🌐 Mock BRTA API

Simulation of

- Driving License Verification
- Vehicle Fitness Verification
- Registration Lookup

No real government APIs are used.

---

## 🤖 AI Violation Detection Demo

Concept demonstration using rule-based AI.

Simulates

- Helmet Detection
- Seatbelt Detection
- Number Plate Reading
- Speed Violation Detection

*(Educational demonstration only—not actual computer vision.)*

---

## 🔔 Notification Center

Receive alerts for

- New Violations
- Expiring Documents
- Successful Payments
- Admin Notices
- Appeal Updates

---

# 🛠️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python
- SQLAlchemy ORM

## Database

- SQLite
- PostgreSQL (Production Ready)

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly

## PDF Generation

- ReportLab

## Authentication

- Bcrypt

## Mock Data

- Faker

---

# 🚀 Quick Start

## Prerequisites

- Python 3.10+
- pip

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/rahanul089/drivebd.git

cd drivebd
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Initialize Database

```bash
python -m utils.seed
```

This generates

- drivebd.db
- Sample Users
- Sample Vehicles
- Violations
- Payments
- CSV Files

---

## 5️⃣ Run Application

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# 🔐 Demo Credentials

After running the seed script

| Role | Email | Password |
|------|--------|----------|
| Admin | admin@drivebd.gov.bd | Admin@123 |
| Owner | demo@drivebd.gov.bd | Demo@123 |

Additional randomly generated users can be found inside

```
data/users.csv
```

Default password

```
Password@123
```

---

# ☁️ Deploy to Streamlit Community Cloud

DriveBD is deployment-ready.

## Step 1

Push the project to GitHub.

---

## Step 2

Login to

https://share.streamlit.io/

---

## Step 3

Select your repository.

---

## Step 4

Because Streamlit Cloud uses temporary storage, add this after `init_db()` inside `app.py`.

```python
import os
from utils.db import DB_PATH

if not os.path.exists(DB_PATH):
    from utils.seed import generate
    generate()
```

---

## Step 5

Deploy

Main file

```
app.py
```

---

### 💡 Production Tip

For persistent data storage, configure a PostgreSQL database and set the following environment variable in **Streamlit → Settings → Secrets**:

```text
DATABASE_URL=postgresql://username:password@host:5432/database
```

Recommended free providers:

- Neon
- Supabase
- Railway PostgreSQL

---

# 📂 Project Structure

```text
drivebd/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── auth.py
│   ├── db.py
│   ├── seed.py
│   ├── pdf_utils.py
│   └── helpers.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Vehicles.py
│   ├── 3_Violations.py
│   ├── 4_Payments.py
│   ├── 5_Documents.py
│   ├── 6_Service_History.py
│   ├── 7_Notifications.py
│   ├── 8_Appeals.py
│   ├── 9_Admin.py
│   ├── 10_Reports.py
│   ├── 11_Analytics.py
│   ├── 12_Mock_BRTA_API.py
│   └── 13_AI_Demo.py
│
├── assets/
│
├── data/
│
└── drivebd.db
```

---

# 📸 Screenshots

You can include screenshots here after deployment.

```text
assets/
├── dashboard.png
├── vehicles.png
├── violations.png
├── analytics.png
├── payments.png
```

Example:

```md
## Dashboard

![Dashboard](assets/dashboard.png)

## Analytics

![Analytics](assets/analytics.png)
```

---

# 🔒 Security Features

- Bcrypt Password Hashing
- Role-Based Access Control (RBAC)
- SQLAlchemy ORM Protection
- Session Authentication
- Input Validation
- Protected Admin Pages
- Safe Database Transactions

---

# 🧪 Future Improvements

- OCR-based License Verification
- Real AI Computer Vision
- Live Camera Integration
- BRTA API Integration
- Bangladesh Police API Integration
- SMS Notifications
- Email Verification
- Two-Factor Authentication (2FA)
- Mobile Application (Flutter)
- GPS Vehicle Tracking
- Online Vehicle Tax Payment
- Cloud Storage for Documents

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgments

- Real-world Bangladesh transportation concepts inspired by public BRTA guidelines and transport policies.
- Streamlit for the interactive web framework.
- SQLAlchemy for robust ORM support.
- Plotly for interactive visualizations.
- Pandas and NumPy for efficient data processing.
- Faker for generating realistic synthetic datasets.
- ReportLab for professional PDF generation.
- The Python open-source community for excellent libraries and tooling.

---

# 📬 Contact

**Maintainer:** Rahanul

**GitHub:** https://github.com/rahanul089

**Project Repository:**

https://github.com/rahanul089/drivebd

---

# ⭐ Show Your Support

If you found this project useful, educational, or inspiring, please consider:

- ⭐ Starring the repository on GitHub
- 🍴 Forking the project
- 🐛 Reporting bugs or suggesting improvements
- 💡 Opening feature requests
- 🤝 Contributing through pull requests

Your support helps improve the project and encourages future open-source development.

---

## ❤️ Made with Passion

Made with ❤️ for the people of Bangladesh 🇧🇩

Designed and developed as a portfolio project demonstrating modern software engineering, database design, UI/UX, analytics, and full-stack development using Python and Streamlit.

---

## 📌 Project Status

> 🚀 **Status:** Production-Ready Portfolio Project

Current Version:

```
v1.0.0
```

Last Updated:

```
August 2026
```

Maintained by:

**Rahanul**

---

## 🌟 If you like this project...

```
⭐ Star the repository
🍴 Fork it
📢 Share it
💙 Happy Coding!
```
