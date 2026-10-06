from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

meetings_bp = Blueprint('meetings', __name__)

def sid(): return session.get('society_id')

@meetings_bp.route('/meetings')
def meetings():
    db = get_db()
    mtgs = db.execute('SELECT * FROM meetings WHERE society_id=? ORDER BY meeting_date DESC',(sid(),)).fetchall()
    notices = db.execute('''SELECT mp.*,m.meeting_title,m.meeting_date,m.video_link FROM meeting_points mp
        JOIN meetings m ON mp.meeting_id=m.id WHERE m.society_id=? AND mp.show_as_notice=1
        ORDER BY m.meeting_date DESC,mp.point_no''',(sid(),)).fetchall()
    db.close()
    return render_template('meetings.html', meetings=mtgs, notices=notices)

@meetings_bp.route('/meetings/add', methods=['POST'])
def add_meeting():
    f = request.form; db = get_db()
    vlink = f.get('video_link','').strip()
    if not vlink:
        vlink = f"https://meet.jit.si/SUREKHA_Society_Meeting_{sid()}_{f['meeting_date']}"
    db.execute('INSERT INTO meetings (society_id,meeting_title,meeting_date,meeting_time,venue,video_link) VALUES(?,?,?,?,?,?)',
        (sid(),f['meeting_title'],f['meeting_date'],f['meeting_time'],f.get('venue',''),vlink))
    mid = db.execute('SELECT last_insert_rowid() as id').fetchone()['id']
    for i,pt in enumerate(f.getlist('agenda_point')):
        if pt.strip():
            db.execute('INSERT INTO meeting_points (meeting_id,point_no,agenda_point,show_as_notice) VALUES(?,?,?,1)',
                (mid,i+1,pt.strip()))
    db.commit(); db.close()
    flash('Meeting & Video Room scheduled successfully!', 'success')
    return redirect(url_for('meetings.meetings'))

@meetings_bp.route('/meetings/delete/<int:mid>')
def delete_meeting(mid):
    db = get_db()
    db.execute('DELETE FROM meeting_points WHERE meeting_id=?',(mid,))
    db.execute('DELETE FROM meetings WHERE id=?',(mid,))
    db.commit(); db.close()
    return redirect(url_for('meetings.meetings'))
