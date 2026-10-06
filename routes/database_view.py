from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import get_db

database_view_bp = Blueprint('database_view', __name__)

TABLES = ['firm','societies','members','ij_share_forms','receipts','payments',
          'journal','ledger','cash_bank','billing_charges','bills','meetings','meeting_points']

@database_view_bp.route('/database-view')
def database_view():
    if 'firm_id' not in session: return redirect(url_for('auth.login'))
    db = get_db()
    selected_table = request.args.get('table', 'firm')
    if selected_table not in TABLES: selected_table = 'firm'
    rows = db.execute(f"SELECT * FROM {selected_table} LIMIT 200").fetchall()
    columns = list(rows[0].keys()) if rows else []
    table_counts = {t: db.execute(f"SELECT COUNT(*) as c FROM {t}").fetchone()['c'] for t in TABLES}
    db.close()
    return render_template('database_view.html', tables=TABLES, selected_table=selected_table,
                           columns=columns, rows=rows, table_counts=table_counts)

@database_view_bp.route('/database-view/delete/<table>/<int:row_id>')
def delete_record(table, row_id):
    if 'firm_id' not in session: return redirect(url_for('auth.login'))
    if table not in TABLES:
        flash('Invalid table!', 'error')
        return redirect(url_for('database_view.database_view'))
    db = get_db()
    db.execute(f"DELETE FROM {table} WHERE id=?", (row_id,))
    db.commit(); db.close()
    flash(f'Record #{row_id} deleted from {table}!', 'success')
    return redirect(url_for('database_view.database_view', table=table))

@database_view_bp.route('/database-view/delete-all/<table>', methods=['POST'])
def delete_all_records(table):
    if 'firm_id' not in session: return redirect(url_for('auth.login'))
    if table not in TABLES:
        flash('Invalid table!', 'error')
        return redirect(url_for('database_view.database_view'))
    db = get_db()
    db.execute(f"DELETE FROM {table}")
    db.commit(); db.close()
    flash(f'All records deleted from {table}!', 'success')
    return redirect(url_for('database_view.database_view', table=table))
