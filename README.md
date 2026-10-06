# 🏢 SUREKHA
### Smart Urban Residential Estate & Knowledge-based Housing Accounting

A modular web-based Housing Society Management Platform built using **Python Flask** and **SQLite3**, adhering to statutory standards under the Maharashtra Co-operative Societies Act.

---

## 🌟 Key Modules

1. **🔐 Authentication & Society Setup:** Multi-society management under a master firm account, secure session management, and real-time password recovery via Gmail SMTP SSL.
2. **👥 Members & Statutory Registers:** Resident registration, auto-generation of Maharashtra **Form I** (Register of Members), **Form J** (List of Members), and Share Certificates.
3. **💰 Billing & Financial Accounting:** 19-Item statutory maintenance receipts, batch bill generation, number-to-words currency translation, and double-entry ledgers / cash-bank books.
4. **📊 Final Accounts & Reporting:** Income & Expenditure accounts, balance sheets, and real-time member outstanding dues tracking.
5. **🤝 Digital Meetings & Communication:** AGM/EGM scheduling with auto-generated **Jitsi Meet** video conferencing links and interactive society notice board.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+ (Flask Framework with Modular Blueprint Architecture)
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Template Engine
- **Database:** SQLite 3 (`surekha.db`) with 13 relational tables
- **External APIs:** Google Gmail SMTP (`smtp.gmail.com:465`), Jitsi Meet API

---

## 🚀 How to Run Locally

### 1. Clone or Download Repository
```bash
git clone https://github.com/your-username/SUREKHA.git
cd SUREKHA
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Launch Application
```bash
python app.py
```
*(On Windows, you can simply double-click `RUN_SUREKHA.bat`)*

### 4. Access the Platform
Open your browser and visit:
```
http://127.0.0.1:5000
```

---

## 📁 Project Directory Structure
```
SUREKHA/
├── app.py                  # Main Application Entry Point
├── database.py             # Database Schema & SQLite Helper Functions
├── requirements.txt        # Python Dependencies List
├── RUN_SUREKHA.bat         # 1-Click Desktop Launcher
├── routes/                 # Blueprint Route Controllers
│   ├── auth.py
│   ├── society.py
│   ├── members.py
│   ├── registers.py
│   ├── billing.py
│   ├── entries.py
│   ├── accounts.py
│   ├── reports.py
│   └── meetings.py
├── templates/              # HTML Templates (Jinja2)
└── static/                 # CSS Stylesheets & JavaScript
```
