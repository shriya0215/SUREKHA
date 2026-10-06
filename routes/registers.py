from flask import Blueprint, render_template, request, session
from database import get_db

registers_bp = Blueprint('registers', __name__)

def sid(): return session.get('society_id')

@registers_bp.route('/registers')
def registers():
    db = get_db()
    ftype = request.args.get('type','I')
    forms = db.execute('''SELECT f.*,m.name,m.flat_no FROM ij_share_forms f
        LEFT JOIN members m ON f.member_id=m.id
        WHERE f.society_id=? AND f.form_type=? ORDER BY f.form_date''',(sid(),ftype)).fetchall()
    members = db.execute('SELECT * FROM members WHERE society_id=? ORDER BY flat_no',(sid(),)).fetchall()
    db.close()
    return render_template('registers.html', forms=forms, form_type=ftype, members=members)

@registers_bp.route('/registers/print/form-i')
def print_form_i():
    db = get_db()
    soc = db.execute('SELECT * FROM societies WHERE id=?',(sid(),)).fetchone()
    members = db.execute('SELECT * FROM members WHERE society_id=? ORDER BY flat_no',(sid(),)).fetchall()
    db.close()
    return render_template('form_i_print.html', society=soc, members=members)

@registers_bp.route('/registers/print/form-j')
def print_form_j():
    db = get_db()
    soc = db.execute('SELECT * FROM societies WHERE id=?',(sid(),)).fetchone()
    members = db.execute('SELECT * FROM members WHERE society_id=? ORDER BY flat_no',(sid(),)).fetchall()
    db.close()
    return render_template('form_j_print.html', society=soc, members=members)

@registers_bp.route('/registers/print/share-cert/<int:mid>')
def print_share_cert(mid):
    db = get_db()
    soc = db.execute('SELECT * FROM societies WHERE id=?',(sid(),)).fetchone()
    member = db.execute('SELECT * FROM members WHERE id=?',(mid,)).fetchone()
    db.close()
    return render_template('share_cert_print.html', society=soc, member=member)
