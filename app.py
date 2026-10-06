from flask import Flask
from database import init_db
from routes.auth          import auth_bp
from routes.society       import society_bp
from routes.members       import members_bp
from routes.entries       import entries_bp
from routes.billing       import billing_bp
from routes.accounts      import accounts_bp
from routes.reports       import reports_bp
from routes.registers     import registers_bp
from routes.meetings      import meetings_bp
from routes.database_view import database_view_bp

app = Flask(__name__)
app.secret_key = 'surekha_secret_2024'

app.register_blueprint(auth_bp)
app.register_blueprint(society_bp)
app.register_blueprint(members_bp)
app.register_blueprint(entries_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(registers_bp)
app.register_blueprint(meetings_bp)
app.register_blueprint(database_view_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True, use_reloader=False)
