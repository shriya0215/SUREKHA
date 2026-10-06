import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), 'surekha.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS firm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_name TEXT, operation_type TEXT, admin_name TEXT,
        contact_no TEXT, email TEXT, address TEXT, scale_societies INTEGER,
        member_tier TEXT, period_start TEXT,
        username TEXT UNIQUE, password TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS societies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_id INTEGER, society_name TEXT, register_no TEXT,
        register_date TEXT, address TEXT, no_of_members INTEGER DEFAULT 0,
        start_form TEXT, rate_of_interest REAL DEFAULT 18.0,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, member_type TEXT DEFAULT 'Single',
        name TEXT, joint_name TEXT, flat_no TEXT, building_no TEXT,
        share_cert_no TEXT, mobile TEXT, email TEXT, nomination TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS ij_share_forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, form_type TEXT, member_id INTEGER,
        form_date TEXT, details TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, sno TEXT, receipt_date TEXT,
        received_from TEXT, flat_no TEXT, building_no TEXT,
        entrance_fees REAL DEFAULT 0, shares REAL DEFAULT 0,
        deposits REAL DEFAULT 0, loan_installments REAL DEFAULT 0,
        interest_on_loan REAL DEFAULT 0, interest_defaulted REAL DEFAULT 0,
        contribution_construction REAL DEFAULT 0, lease_rent REAL DEFAULT 0,
        municipal_taxes REAL DEFAULT 0, water_charges REAL DEFAULT 0,
        electricity_charges REAL DEFAULT 0, parking_charges REAL DEFAULT 0,
        lift_charges REAL DEFAULT 0, sinking_fund REAL DEFAULT 0,
        service_charges REAL DEFAULT 0, insurance REAL DEFAULT 0,
        suspense_share_capital REAL DEFAULT 0, donations REAL DEFAULT 0,
        miscellaneous REAL DEFAULT 0, total REAL DEFAULT 0,
        payment_mode TEXT DEFAULT 'Cash', narration TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, payment_date TEXT, payee_name TEXT,
        particulars TEXT, amount REAL DEFAULT 0,
        payment_mode TEXT DEFAULT 'Cash', cheque_no TEXT, narration TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, journal_date TEXT,
        debit_account TEXT, credit_account TEXT,
        amount REAL DEFAULT 0, narration TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, account_name TEXT, entry_date TEXT,
        entry_type TEXT, amount REAL DEFAULT 0,
        balance REAL DEFAULT 0, narration TEXT,
        ref_type TEXT, ref_id INTEGER,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS cash_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, entry_date TEXT,
        account_type TEXT DEFAULT 'Cash', particulars TEXT,
        debit REAL DEFAULT 0, credit REAL DEFAULT 0,
        balance REAL DEFAULT 0, narration TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS billing_charges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER UNIQUE,
        maintenance_service REAL DEFAULT 450,
        repair_fund REAL DEFAULT 300,
        car_parking REAL DEFAULT 180,
        noc REAL DEFAULT 150,
        billing_cycle TEXT DEFAULT 'Monthly'
    );
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, member_id INTEGER, bill_no TEXT,
        bill_date TEXT, due_date TEXT, period_from TEXT, period_to TEXT,
        municipal_dues REAL DEFAULT 0, admin_expenses REAL DEFAULT 0,
        sinking_funds REAL DEFAULT 0, periodic_maintenance REAL DEFAULT 0,
        parking REAL DEFAULT 0, noc_misc REAL DEFAULT 0,
        past_arrears REAL DEFAULT 0, interest_due REAL DEFAULT 0,
        total_payable REAL DEFAULT 0, is_paid INTEGER DEFAULT 0,
        generation_mode TEXT DEFAULT 'Auto',
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        society_id INTEGER, meeting_title TEXT,
        meeting_date TEXT, meeting_time TEXT, venue TEXT, video_link TEXT,
        created_at TEXT DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS meeting_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meeting_id INTEGER, point_no INTEGER,
        agenda_point TEXT, show_as_notice INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (date('now'))
    );
    ''')
    try:
        c.execute('ALTER TABLE firm ADD COLUMN email TEXT')
        conn.commit()
    except: pass
    conn.close()
