from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import random, os, re
from datetime import datetime, date
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

auth = Blueprint('auth', __name__)
USERS = {}

def compute_age(dob_str):
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            dob_date = datetime.strptime(dob_str, fmt).date()
            today = date.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            return age
        except Exception:
            continue
    return ""

def extract_info_from_id(file_path):
    extracted_text = ""
    if pytesseract:
        try:
            image = Image.open(file_path)
            image = image.convert('L')
            image = image.point(lambda x: 0 if x < 140 else 255, '1')
            custom_config = r'--oem 3 --psm 6'
            extracted_text = pytesseract.image_to_string(image, config=custom_config)
        except Exception as e:
            extracted_text = ""

    name = ""
    dob = ""
    age = ""
    gender = ""
    address = ""

    name_match = re.search(r'NAME[:\-\s]*([\w\s]+)', extracted_text, re.IGNORECASE)
    if name_match:
        name = name_match.group(1).strip()


    dob_match = re.search(r'(\d{2}[\/\-]\d{2}[\/\-]\d{4}|\d{4}[\/\-]\d{2}[\/\-]\d{2})', extracted_text)
    if dob_match:
        dob = dob_match.group(0).strip()
        age = compute_age(dob)

    if re.search(r'\bMALE\b', extracted_text, re.IGNORECASE):
        gender = "Male"
    elif re.search(r'\bFEMALE\b', extracted_text, re.IGNORECASE):
        gender = "Female"

    address_match = re.search(r'ADDRESS[:\-\s]*(.*)', extracted_text, re.IGNORECASE)
    if address_match:
        address = address_match.group(1).strip()

    return {"name": name, "dob": dob, "age": age, "gender": gender, "address": address}

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        otp = str(random.randint(100000, 999999))
        session['signup_email'] = email
        session['signup_otp'] = otp
        flash(f"Simulated OTP sent: {otp}", "info")  
        return redirect(url_for('auth.verify_signup'))
    return render_template('signup.html')

@auth.route('/verify_signup', methods=['GET', 'POST'])
def verify_signup():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('signup_otp'):
            return redirect(url_for('auth.personal_details'))
        else:
            flash("Incorrect OTP. Try again.", "error")
    return render_template('verify_signup.html')

@auth.route('/personal_details', methods=['GET', 'POST'])
def personal_details():
    extracted = {"name": "", "dob": "", "age": "", "gender": "", "address": ""}
    if request.method == 'POST':
        if 'id_proof' in request.files and request.files['id_proof'].filename != "":
            file = request.files['id_proof']
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            extracted = extract_info_from_id(file_path)
        if request.form.get('confirm'):
            email = session.get('signup_email')
            full_name = request.form.get('name')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            address = request.form.get('address')
            USERS[email] = {
                "name": full_name,
                "dob": dob,
                "gender": gender,
                "address": address,
                "email": email
            }
            flash("Signup complete! You can now log in.", "success")
            return redirect(url_for('auth.login'))
    return render_template('personal_details.html', extracted=extracted)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS:
            otp = str(random.randint(100000, 999999))
            session['login_email'] = email
            session['login_otp'] = otp
            flash(f"Simulated OTP sent: {otp}", "info")
            return redirect(url_for('auth.verify_login'))
        else:
            flash("Email not found. Please sign up.", "error")
    return render_template('login.html')

@auth.route('/verify_login', methods=['GET', 'POST'])
def verify_login():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('login_otp'):
            session['user'] = session.get('login_email')
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect OTP. Try again.", "error")
    return render_template('verify_login.html')
