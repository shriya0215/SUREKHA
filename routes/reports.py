from flask import Blueprint, render_template, session
from database import get_db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def reports():
    db = get_db(); sid = session.get('society_id')
    outstanding = db.execute('''SELECT m.name,m.flat_no,m.mobile,
        COUNT(b.id) as unpaid_count, COALESCE(SUM(b.total_payable),0) as total_due
        FROM members m LEFT JOIN bills b ON m.id=b.member_id AND b.is_paid=0
        WHERE m.society_id=? GROUP BY m.id HAVING unpaid_count > 0''',(sid,)).fetchall()
    all_members = db.execute('SELECT * FROM members WHERE society_id=? ORDER BY flat_no',(sid,)).fetchall()
    db.close()
    return render_template('reports.html', outstanding=outstanding, all_members=all_members)
