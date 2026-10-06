from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db
import random, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint('auth', __name__)

# ── Gmail SMTP Config ──────────────────────────────────────────────────────────
GMAIL_USER = "takaleshriya25@gmail.com"   # Gmail Sender ID
GMAIL_PASS = "elde uqkq gyob inxj"         # Gmail App Password (16-digit)

def send_real_email(to_email, otp_code):
    """Sends real OTP Email via Gmail SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔑 SUREKHA Password Reset OTP'
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;border:1px solid #ddd;border-radius:12px;overflow:hidden;">
          <div style="background:#1a237e;padding:20px;text-align:center;">
            <h2 style="color:#f9a825;margin:0;">SURE<span style="color:#fff;">KHA</span></h2>
            <p style="color:#fff;margin:4px 0;font-size:13px;">Housing Society Management Platform</p>
          </div>
          <div style="padding:24px;">
            <h3 style="color:#1a237e;">Password Reset OTP</h3>
            <p style="color:#555;">Your One-Time Password (OTP) for SUREKHA password reset is:</p>
            <div style="background:#f0f2f5;border-radius:10px;padding:18px;text-align:center;margin:20px 0;">
              <span style="font-size:36px;font-weight:900;letter-spacing:10px;color:#1a237e;">{otp_code}</span>
            </div>
            <p style="color:#888;font-size:12px;">This OTP is valid for 10 minutes. Do NOT share it with anyone.</p>
          </div>
        </div>"""
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f"[EMAIL SENT] OTP {otp_code} → {to_email}")
        return True, "Email sent!"
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False, str(e)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.dashboard') if 'firm_id' in session else url_for('auth.login'))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        firm = db.execute('SELECT * FROM firm WHERE username=? AND password=?',
                          (request.form['username'], request.form['password'])).fetchone()
        db.close()
        if firm:
            session['firm_id'] = firm['id']; session['firm_name'] = firm['firm_name']
            return redirect(url_for('auth.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        f = request.form; db = get_db()
        try:
            db.execute('''INSERT INTO firm (firm_name,operation_type,admin_name,contact_no,
                email,address,scale_societies,member_tier,period_start,username,password)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                (f['firm_name'],f['operation_type'],f['admin_name'],f['contact_no'],
                 f.get('email',''),f['address'],f['scale_societies'],f['member_tier'],
                 f['period_start'],f['username'],f['password']))
            db.commit()
            flash('Firm registered! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Username already exists!', 'error')
        finally: db.close()
    return render_template('firm_register.html')

@auth_bp.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    step = 'send'; email_hint = ''
    if request.method == 'POST':
        action = request.form.get('action'); db = get_db()
        if action == 'send_otp':
            u = request.form['username']; em = request.form['email']
            firm = db.execute('SELECT * FROM firm WHERE username=? AND (email=? OR contact_no=?)',(u,em,em)).fetchone()
            if firm:
                otp = str(random.randint(100000, 999999))
                session['reset_otp'] = otp; session['reset_firm_id'] = firm['id']
                target_mail = firm['email'] if firm['email'] else em
                ok, err = send_real_email(target_mail, otp)
                if ok:
                    flash(f'📧 OTP sent to {target_mail}. Check your Inbox / Spam folder!', 'success')
                else:
                    flash(f'❌ Email Error: {err}', 'error')
                step = 'verify'; email_hint = target_mail
            else:
                flash('Username or Email does not match!', 'error')
            db.close()
        elif action == 'verify_otp':
            entered = request.form.get('otp',''); new_pass = request.form.get('new_password','')
            if entered == session.get('reset_otp'):
                fid = session.get('reset_firm_id')
                db.execute('UPDATE firm SET password=? WHERE id=?',(new_pass, fid))
                db.commit(); db.close()
                session.pop('reset_otp', None); session.pop('reset_firm_id', None)
                flash('✅ Password reset successfully! Please login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                db.close()
                flash('❌ Invalid OTP! Please check your Email inbox.', 'error'); step = 'verify'
    return render_template('forgot_password.html', step=step, email_hint=email_hint)

@auth_bp.route('/logout')
def logout():
    session.clear(); return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'firm_id' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    societies = db.execute('SELECT * FROM societies WHERE firm_id=?',(session['firm_id'],)).fetchall()
    total_members = sum(db.execute('SELECT COUNT(*) as c FROM members WHERE society_id=?',(s['id'],)).fetchone()['c'] for s in societies)
    total_bills = sum(db.execute('SELECT COUNT(*) as c FROM bills WHERE society_id=? AND is_paid=0',(s['id'],)).fetchone()['c'] for s in societies)
    db.close()
    return render_template('home.html', societies=societies, total_societies=len(societies), total_members=total_members, total_outstanding=total_bills)
