# 🚀 HelperMS  
## AI-Driven HR Management System (Prototype)

HelperMS is an **AI-powered HR platform prototype** designed to simplify hiring and HR workflows.  
From **smart resume screening** to **automated interview scheduling**, **email generation**, and **live HR analytics** — HelperMS brings intelligence and automation into one clean dashboard.

Built for **Google Girl Hackathon SWE 2025** 💙

---

## 🌟 Features

### 📄 Resume Screening & Smart Candidate Ranking
- Upload and analyze resumes  
- Select a job role  
- Automatically ranks candidates by **years of experience**

### 📅 Automated Interview Scheduling
- Schedule interviews with:
  - Candidate name  
  - Role  
  - Date  
  - Time  
  - Interviewer  
- View all scheduled interviews in one place  
- Stored persistently in the database  

### ✉ Smart Email Generator
- Enter candidate name and purpose  
- Instantly generate a professional HR email  
- All generated emails are saved  

### 📊 HR Analytics Dashboard
Live statistics from the system:
- Total registered users  
- Total login attempts  
- Total interviews scheduled  
- Total emails generated  

---

## 🔐 Authentication

### Signup
- First name, last name  
- Age, gender  
- Organization email  

### Login
- Username (first name or full name)  
- Organization email  

**Demo login**
```
Username: john  
Email: john@gmail.com
```

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | HTML, CSS (custom dark UI) |
| Backend | Flask |
| Database | SQLite |
| AI / NLP | Sentence Transformers, PyMuPDF, Pillow |
| Machine Learning | Resume ranking engine |
| Authentication | Flask Blueprints + SQLite |

---

## 📁 Project Structure

```
Google-Girl-Hackathon_SWE_2025-main/
├── app.py                 # Main Flask app
├── auth.py                # Authentication & DB logic
├── resume_processing.py  # Resume ranking logic
├── helperms.db            # SQLite database
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── resume_screening.html
│   ├── interview_scheduling.html
│   ├── smart_email.html
│   ├── hr_analytics.html
│   ├── login.html
│   └── signup.html
├── static/
│   └── style.css
└── requirements.txt
```

---

## ▶ How to Run Locally

```bash
git clone https://github.com/devyanighildiyal/Google-Girl-Hackathon_SWE_2025.git
cd Google-Girl-Hackathon_SWE_2025
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open in your browser:
```
http://127.0.0.1:5000
```

---

## 📊 Database Tables

| Table | Purpose |
|------|---------|
| users | Stores signup details |
| login_events | Logs login attempts |
| interviews | Stores interview schedules |
| emails | Stores generated emails |

---

## 👩‍💻 Author

**Devyani Ghildiyal**  
Google Girl Hackathon SWE 2025  
