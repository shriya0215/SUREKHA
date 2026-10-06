from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

society_bp = Blueprint('society', __name__)

def login_req():
    return 'firm_id' not in session

@society_bp.route('/societies')
def societies():
    if login_req(): return redirect(url_for('auth.login'))
    db = get_db()
    rows = db.execute('SELECT * FROM societies WHERE firm_id=?',
                      (session['firm_id'],)).fetchall()
    db.close()
    return render_template('society_management.html', societies=rows, show_form=False)

@society_bp.route('/societies/add', methods=['GET','POST'])
def add_society():
    if login_req(): return redirect(url_for('auth.login'))
    if request.method == 'POST':
        f = request.form
        db = get_db()
        db.execute('''INSERT INTO societies (firm_id,society_name,register_no,
            register_date,address,no_of_members,start_form,rate_of_interest)
            VALUES(?,?,?,?,?,?,?,?)''',
            (session['firm_id'],f['society_name'],f['register_no'],
             f['register_date'],f['address'],f['no_of_members'],
             f['start_form'],f['rate_of_interest']))
        db.commit(); db.close()
        flash('Society added!', 'success')
        return redirect(url_for('society.societies'))
    return render_template('society_management.html', societies=[], show_form=True)

@society_bp.route('/societies/select/<int:sid>')
def select_society(sid):
    if login_req(): return redirect(url_for('auth.login'))
    db = get_db()
    soc = db.execute('SELECT * FROM societies WHERE id=? AND firm_id=?',
                     (sid, session['firm_id'])).fetchone()
    db.close()
    if soc:
        session['society_id'] = sid
        session['society_name'] = soc['society_name']
    return redirect(url_for('auth.dashboard'))

@society_bp.route('/societies/delete/<int:sid>')
def delete_society(sid):
    if login_req(): return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('DELETE FROM societies WHERE id=? AND firm_id=?',
               (sid, session['firm_id']))
    db.commit(); db.close()
    if session.get('society_id') == sid:
        session.pop('society_id', None)
        session.pop('society_name', None)
    return redirect(url_for('society.societies'))
