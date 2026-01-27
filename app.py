from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps

from auth import auth
from resume_processing import get_occupations, process_resume_dataset

import sqlite3
from datetime import datetime

DB_PATH = "helperms.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(view_func):
    """Simple auth guard for routes that require a logged-in user."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("user_email"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapper

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.register_blueprint(auth)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/resume_screening', methods=['GET', 'POST'])
@login_required
def resume_screening():
    if request.method == 'POST':
        occupation = request.form.get('occupation')
        results = process_resume_dataset(occupation)
        occupations = get_occupations()
        return render_template('resume_screening.html', results=results, selected_occupation=occupation, occupations=occupations)
    else:
        occupations = get_occupations()
        return render_template('resume_screening.html', results=None, occupations=occupations)


# --- Placeholder module routes (Modules 2–6) ---

@app.route('/interview_scheduling', methods=['GET','POST'])
@login_required
def interview_scheduling():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("""
            INSERT INTO interviews
            (candidate, role, date, time, interviewer, created_by_email, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form['candidate'],
            request.form['role'],
            request.form['date'],
            request.form['time'],
            request.form['interviewer'],
            session.get("user_email"),
            datetime.utcnow().isoformat()
        ))
        conn.commit()

    cur.execute("SELECT * FROM interviews ORDER BY date, time")
    interviews = cur.fetchall()
    conn.close()
    return render_template('interview_scheduling.html', interviews=interviews)



@app.route('/smart_email', methods=['GET','POST'])
@login_required
def smart_email():
    generated = None

    if request.method == 'POST':
        name = request.form['name']
        purpose = request.form['purpose']
        generated = f"""Dear {name},

We are pleased to inform you regarding {purpose}.

Please confirm your availability.

Best regards,
HR Team"""

        conn = get_db()
        conn.execute("""
            INSERT INTO emails
            (recipient_name, purpose, content, created_by_email, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, purpose, generated, session.get("user_email"), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

    return render_template('smart_email.html', email=generated)



@app.route('/hr_analytics')
@login_required
def hr_analytics():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM login_events")
    logins = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM interviews")
    interviews = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM emails")
    emails = cur.fetchone()[0]

    conn.close()
    return render_template("hr_analytics.html",
        total_users=users,
        total_logins=logins,
        total_interviews=interviews,
        total_emails=emails
    )

if __name__ == '__main__':
    app.run(debug=True)
