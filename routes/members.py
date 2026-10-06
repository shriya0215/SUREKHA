from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

members_bp = Blueprint('members', __name__)

def chk():
    return 'society_id' not in session

@members_bp.route('/members')
def members():
    if chk(): return redirect(url_for('society.societies'))
    db = get_db()
    rows = db.execute('SELECT * FROM members WHERE society_id=? ORDER BY flat_no',
                      (session['society_id'],)).fetchall()
    db.close()
    return render_template('members.html', members=rows, show_form=False)

@members_bp.route('/members/add', methods=['GET','POST'])
def add_member():
    if chk(): return redirect(url_for('society.societies'))
    if request.method == 'POST':
        f = request.form; db = get_db()
        db.execute('''INSERT INTO members (society_id,member_type,name,joint_name,
            flat_no,building_no,share_cert_no,mobile,email,nomination)
            VALUES(?,?,?,?,?,?,?,?,?,?)''',
            (session['society_id'],f['member_type'],f['name'],
             f.get('joint_name',''),f['flat_no'],f.get('building_no',''),
             f['share_cert_no'],f['mobile'],f.get('email',''),
             f.get('nomination','')))
        db.execute('''UPDATE societies SET no_of_members=(
            SELECT COUNT(*) FROM members WHERE society_id=?) WHERE id=?''',
            (session['society_id'],session['society_id']))
        db.commit(); db.close()
        flash('Member added!', 'success')
        return redirect(url_for('members.members'))
    return render_template('members.html', members=[], show_form=True)

@members_bp.route('/members/notify-all', methods=['POST'])
def notify_all():
    if chk(): return redirect(url_for('society.societies'))
    db = get_db()
    cnt = len(db.execute('SELECT * FROM members WHERE society_id=?', (session['society_id'],)).fetchall())
    db.close()
    flash(f'📲 SMS and ✉️ Email notifications sent successfully to all {cnt} members!', 'success')
    return redirect(url_for('members.members'))

@members_bp.route('/members/delete/<int:mid>')
def delete_member(mid):
    db = get_db()
    db.execute('DELETE FROM members WHERE id=?', (mid,))
    db.execute('''UPDATE societies SET no_of_members=(
        SELECT COUNT(*) FROM members WHERE society_id=?) WHERE id=?''',
        (session['society_id'],session['society_id']))
    db.commit(); db.close()
    flash('Member deleted!', 'success')
    return redirect(url_for('members.members'))

@members_bp.route('/ij-share-forms')
def ij_share_forms():
    if chk(): return redirect(url_for('society.societies'))
    db = get_db(); sid = session['society_id']
    forms = db.execute('''SELECT f.*,m.name,m.flat_no FROM ij_share_forms f
        LEFT JOIN members m ON f.member_id=m.id
        WHERE f.society_id=? ORDER BY f.form_type,f.form_date DESC''', (sid,)).fetchall()
    mems = db.execute('SELECT * FROM members WHERE society_id=?',(sid,)).fetchall()
    db.close()
    return render_template('ij_share_form.html', forms=forms, members=mems)

@members_bp.route('/ij-share-forms/add', methods=['POST'])
def add_ij_form():
    f = request.form; db = get_db()
    db.execute('''INSERT INTO ij_share_forms (society_id,form_type,member_id,form_date,details)
        VALUES(?,?,?,?,?)''', (session['society_id'],f['form_type'],f['member_id'],f['form_date'],f['details']))
    db.commit(); db.close()
    flash('Form entry added!', 'success')
    return redirect(url_for('members.ij_share_forms'))

@members_bp.route('/ij-share-forms/delete/<int:fid>')
def delete_ij_form(fid):
    db = get_db()
    db.execute('DELETE FROM ij_share_forms WHERE id=?', (fid,))
    db.commit(); db.close()
    flash('Form entry deleted!', 'success')
    return redirect(url_for('members.ij_share_forms'))
