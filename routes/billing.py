from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db
from datetime import date, timedelta

billing_bp = Blueprint('billing', __name__)
def sid(): return session.get('society_id')

def num_words(n):
    o = ['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
    t = ['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
    def h(n):
        if n==0: return ''
        elif n<20: return o[n]+' '
        elif n<100: return t[n//10]+' '+h(n%10)
        elif n<1000: return o[n//100]+' Hundred '+h(n%100)
        elif n<100000: return h(n//1000)+'Thousand '+h(n%1000)
        elif n<10000000: return h(n//100000)+'Lakh '+h(n%100000)
        else: return h(n//10000000)+'Crore '+h(n%10000000)
    return h(int(n)).strip()+' Only'

@billing_bp.route('/billing')
def billing():
    db = get_db()
    bills = db.execute('SELECT b.*,m.name,m.flat_no FROM bills b JOIN members m ON b.member_id=m.id WHERE b.society_id=? ORDER BY b.bill_date DESC',(sid(),)).fetchall()
    charges = db.execute('SELECT * FROM billing_charges WHERE society_id=?',(sid(),)).fetchone()
    mems = db.execute('SELECT * FROM members WHERE society_id=?',(sid(),)).fetchall(); db.close()
    return render_template('billing.html', bills=bills, charges=charges, members=mems)

@billing_bp.route('/billing/config', methods=['POST'])
def billing_config():
    f = request.form; db = get_db()
    ex = db.execute('SELECT id FROM billing_charges WHERE society_id=?',(sid(),)).fetchone()
    if ex:
        db.execute('UPDATE billing_charges SET maintenance_service=?,repair_fund=?,car_parking=?,noc=?,billing_cycle=? WHERE society_id=?',
            (f['maintenance_service'],f['repair_fund'],f['car_parking'],f['noc'],f['billing_cycle'],sid()))
    else:
        db.execute('INSERT INTO billing_charges (society_id,maintenance_service,repair_fund,car_parking,noc,billing_cycle) VALUES(?,?,?,?,?,?)',
            (sid(),f['maintenance_service'],f['repair_fund'],f['car_parking'],f['noc'],f['billing_cycle']))
    db.commit(); db.close(); flash('Charges updated!', 'success'); return redirect(url_for('billing.billing'))

@billing_bp.route('/billing/generate', methods=['POST'])
def generate_bills():
    f = request.form; db = get_db()
    charges = db.execute('SELECT * FROM billing_charges WHERE society_id=?',(sid(),)).fetchone()
    mems = db.execute('SELECT * FROM members WHERE society_id=?',(sid(),)).fetchall()
    bd = f.get('bill_date', date.today().isoformat()); dd = (date.fromisoformat(bd)+timedelta(days=20)).isoformat()
    cnt = db.execute('SELECT COUNT(*) as c FROM bills WHERE society_id=?',(sid(),)).fetchone()['c']; mode = f.get('mode','Auto')
    for i,m in enumerate(mems):
        mn = float(charges['maintenance_service'] if charges else 450); rf = float(charges['repair_fund'] if charges else 300)
        cp = float(charges['car_parking'] if charges else 180); nc = float(charges['noc'] if charges else 150)
        if mode == 'Manual': mn = float(f.get(f'main_{m["id"]}', mn) or mn); cp = float(f.get(f'park_{m["id"]}', cp) or cp)
        total = mn + rf + cp + nc
        db.execute('INSERT INTO bills (society_id,member_id,bill_no,bill_date,due_date,period_from,period_to,periodic_maintenance,sinking_funds,parking,noc_misc,total_payable,generation_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (sid(),m['id'],f'BILL-{sid()}-{cnt+i+1:04d}',bd,dd,f.get('period_from',''),f.get('period_to',''),mn,rf,cp,nc,total,mode))
    db.commit(); db.close(); flash(f'{len(mems)} bills generated!', 'success'); return redirect(url_for('billing.billing'))

@billing_bp.route('/billing/print/<int:bid>')
def print_bill(bid):
    db = get_db(); bill = db.execute('SELECT b.*,m.name,m.flat_no,m.building_no,s.society_name,s.address,s.register_no,s.rate_of_interest FROM bills b JOIN members m ON b.member_id=m.id JOIN societies s ON b.society_id=s.id WHERE b.id=?',(bid,)).fetchone(); db.close()
    return render_template('billing_print.html', bill=bill, words=num_words(bill['total_payable']))

@billing_bp.route('/billing/paid/<int:bid>')
def mark_paid(bid):
    db = get_db(); db.execute('UPDATE bills SET is_paid=1 WHERE id=?',(bid,)); db.commit(); db.close()
    return redirect(url_for('billing.billing'))

@billing_bp.route('/billing/delete/<int:bid>')
def delete_bill(bid):
    db = get_db(); db.execute('DELETE FROM bills WHERE id=?',(bid,)); db.commit(); db.close()
    flash('Bill deleted!', 'success'); return redirect(url_for('billing.billing'))
