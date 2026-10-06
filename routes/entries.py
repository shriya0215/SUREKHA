from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

entries_bp = Blueprint('entries', __name__)
ITEMS = ['entrance_fees','shares','deposits','loan_installments','interest_on_loan',
         'interest_defaulted','contribution_construction','lease_rent','municipal_taxes',
         'water_charges','electricity_charges','parking_charges','lift_charges',
         'sinking_fund','service_charges','insurance','suspense_share_capital',
         'donations','miscellaneous']

def sid(): return session.get('society_id')

@entries_bp.route('/entries/receipt')
def receipt():
    db = get_db(); rows = db.execute('SELECT * FROM receipts WHERE society_id=? ORDER BY receipt_date DESC',(sid(),)).fetchall(); db.close()
    return render_template('entries_receipt.html', receipts=rows)

@entries_bp.route('/entries/receipt/add', methods=['POST'])
def add_receipt():
    f = request.form; total = sum(float(f.get(i,0) or 0) for i in ITEMS); db = get_db()
    cnt = db.execute('SELECT COUNT(*) as c FROM receipts WHERE society_id=?',(sid(),)).fetchone()['c']
    sno = f'REC-{sid()}-{cnt+1:04d}'
    db.execute(f'INSERT INTO receipts (society_id,sno,receipt_date,received_from,flat_no,building_no,{",".join(ITEMS)},total,payment_mode,narration) VALUES(?,?,?,?,?,?,{",".join(["?"]*19)},?,?,?)',
        (sid(),sno,f['receipt_date'],f['received_from'],f.get('flat_no',''),f.get('building_no',''),*[float(f.get(i,0) or 0) for i in ITEMS],total,f.get('payment_mode','Cash'),f.get('narration','')))
    db.commit(); db.close(); flash(f'Receipt {sno} saved!', 'success')
    return redirect(url_for('entries.receipt'))

@entries_bp.route('/entries/receipt/delete/<int:rid>')
def delete_receipt(rid):
    db = get_db(); db.execute('DELETE FROM receipts WHERE id=?',(rid,)); db.commit(); db.close()
    flash('Receipt deleted!', 'success'); return redirect(url_for('entries.receipt'))

@entries_bp.route('/entries/receipt/print/<int:rid>')
def print_receipt(rid):
    db = get_db(); r = db.execute('SELECT r.*,s.society_name FROM receipts r JOIN societies s ON r.society_id=s.id WHERE r.id=?',(rid,)).fetchone(); db.close()
    return render_template('receipt_print.html', r=r, items=ITEMS)

@entries_bp.route('/entries/payment', methods=['GET','POST'])
def payment():
    db = get_db()
    if request.method == 'POST':
        f = request.form
        db.execute('INSERT INTO payments (society_id,payment_date,payee_name,particulars,amount,payment_mode,cheque_no,narration) VALUES(?,?,?,?,?,?,?,?)',
            (sid(),f['payment_date'],f['payee_name'],f['particulars'],float(f.get('amount',0) or 0),f.get('payment_mode','Cash'),f.get('cheque_no',''),f.get('narration','')))
        db.commit(); flash('Payment saved!', 'success')
    rows = db.execute('SELECT * FROM payments WHERE society_id=? ORDER BY payment_date DESC',(sid(),)).fetchall(); db.close()
    return render_template('entries_payment.html', payments=rows)

@entries_bp.route('/entries/payment/delete/<int:pid>')
def delete_payment(pid):
    db = get_db(); db.execute('DELETE FROM payments WHERE id=?',(pid,)); db.commit(); db.close()
    flash('Payment deleted!', 'success'); return redirect(url_for('entries.payment'))

@entries_bp.route('/entries/journal', methods=['GET','POST'])
def journal():
    db = get_db()
    if request.method == 'POST':
        f = request.form
        db.execute('INSERT INTO journal (society_id,journal_date,debit_account,credit_account,amount,narration) VALUES(?,?,?,?,?,?)',
            (sid(),f['journal_date'],f['debit_account'],f['credit_account'],float(f.get('amount',0) or 0),f.get('narration','')))
        db.commit(); flash('Journal saved!', 'success')
    rows = db.execute('SELECT * FROM journal WHERE society_id=? ORDER BY journal_date DESC',(sid(),)).fetchall(); db.close()
    return render_template('entries_journal.html', journals=rows)

@entries_bp.route('/entries/journal/delete/<int:jid>')
def delete_journal(jid):
    db = get_db(); db.execute('DELETE FROM journal WHERE id=?',(jid,)); db.commit(); db.close()
    flash('Journal entry deleted!', 'success'); return redirect(url_for('entries.journal'))

@entries_bp.route('/entries/ledger')
def ledger():
    db = get_db(); acc = request.args.get('account','Cash/Bank')
    accounts = db.execute('SELECT DISTINCT account_name FROM ledger WHERE society_id=?',(sid(),)).fetchall()
    entries = db.execute('SELECT * FROM ledger WHERE society_id=? AND account_name=? ORDER BY entry_date',(sid(),acc)).fetchall(); db.close()
    return render_template('ledger.html', entries=entries, accounts=accounts, current_account=acc)

@entries_bp.route('/entries/cash-bank', methods=['GET','POST'])
def cash_bank():
    db = get_db(); atype = request.args.get('type','Cash')
    if request.method == 'POST':
        f = request.form; atype = f.get('account_type','Cash')
        last = db.execute('SELECT balance FROM cash_bank WHERE society_id=? AND account_type=? ORDER BY id DESC LIMIT 1',(sid(),atype)).fetchone()
        prev = last['balance'] if last else 0; d = float(f.get('debit',0) or 0); cr = float(f.get('credit',0) or 0)
        db.execute('INSERT INTO cash_bank (society_id,entry_date,account_type,particulars,debit,credit,balance,narration) VALUES(?,?,?,?,?,?,?,?)',
            (sid(),f['entry_date'],atype,f['particulars'],d,cr,prev+d-cr,f.get('narration','')))
        db.commit(); flash('Entry saved!', 'success')
    rows = db.execute('SELECT * FROM cash_bank WHERE society_id=? AND account_type=? ORDER BY entry_date',(sid(),atype)).fetchall()
    bal = rows[-1]['balance'] if rows else 0; db.close()
    return render_template('cash_bank.html', entries=rows, account_type=atype, balance=bal)

@entries_bp.route('/entries/cash-bank/delete/<int:cid>')
def delete_cash_bank(cid):
    db = get_db(); atype = request.args.get('type','Cash')
    db.execute('DELETE FROM cash_bank WHERE id=?',(cid,)); db.commit(); db.close()
    flash('Entry deleted!', 'success'); return redirect(url_for('entries.cash_bank', type=atype))
