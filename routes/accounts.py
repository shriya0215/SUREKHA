from flask import Blueprint, render_template, session
from database import get_db

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts')
def accounts():
    db = get_db(); sid = session.get('society_id')
    income = db.execute('SELECT COALESCE(SUM(total),0) as t FROM receipts WHERE society_id=?',(sid,)).fetchone()['t']
    expense = db.execute('SELECT COALESCE(SUM(amount),0) as t FROM payments WHERE society_id=?',(sid,)).fetchone()['t']
    receipts = db.execute('SELECT receipt_date,received_from,total FROM receipts WHERE society_id=? ORDER BY receipt_date DESC LIMIT 20',(sid,)).fetchall()
    payments = db.execute('SELECT payment_date,payee_name,particulars,amount FROM payments WHERE society_id=? ORDER BY payment_date DESC LIMIT 20',(sid,)).fetchall()
    db.close()
    return render_template('accounts.html', income=income, expense=expense,
                           surplus=income-expense, receipts=receipts, payments=payments)
