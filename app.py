from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps

from auth import auth
from resume_processing import get_occupations, process_resume_dataset


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

@app.route('/interview_scheduling')
@login_required
def interview_scheduling():
    return render_template('interview_scheduling.html')


@app.route('/smart_email')
@login_required
def smart_email():
    return render_template('smart_email.html')


@app.route('/hr_analytics')
@login_required
def hr_analytics():
    return render_template('hr_analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
