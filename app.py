from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from auth import auth 
from resume_processing import get_occupations, process_resume_dataset

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.register_blueprint(auth)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/resume_screening', methods=['GET', 'POST'])
def resume_screening():
    if request.method == 'POST':
        occupation = request.form.get('occupation')
        results = process_resume_dataset(occupation)
        occupations = get_occupations()
        return render_template('resume_screening.html', results=results, selected_occupation=occupation, occupations=occupations)
    else:
        occupations = get_occupations()
        return render_template('resume_screening.html', results=None, occupations=occupations)

if __name__ == '__main__':
    app.run(debug=True)
