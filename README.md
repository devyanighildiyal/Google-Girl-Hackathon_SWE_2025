# HelperMS        
AI-Driven HR Platform: An intelligent HR platform prototype that automates tasks like resume screening, onboarding, interview scheduling, and more.

## Table of Contents: 
1) Project Overview
2) Environment Setup
3) How to Run
4) Folder Structure
5) Additional Notes

## Project Overview
The platform aims to follows a structured pipeline:
1) Candidate Submission – Resumes are uploaded in PDF, DOCX, or image formats.
2) Data Extraction & Processing – OCR (Tesseract/Azure Form Recognizer) extracts text, while NLP models (SpaCy, NLTK) structure and preprocess data.
3) AI-Powered Analysis – BERT/RoBERTa and Sentence Transformers perform skill matching, ranking candidates based on job requirements.
4) HR Dashboard – Displays ranked candidates, insights, and analytics.
5) Interview Scheduling – Syncs with Google Calendar API/Microsoft Outlook API.
6) AI Chatbot – Handles HR queries using Rasa/OpenAI GPT API.
7) Email Automation – AI-generated emails for responses, follow-ups, and rejections.
8) Insights & Reporting – Uses Pandas, Matplotlib, and Power BI/Streamlit for visualization.

## Environment Setup

1) Clone the Repository:
   
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

2) Create and Activate a Virtual Environment:
   
python -m venv venv

3) Install Dependencies:

pip install -r requirements.txt


## How to Run:
1) Navigate to the Project Folder:
   
cd <repository-name>

2) Run the Flask App:
   
python app.py

3) Open Your Browser:
   
Visit http://127.0.0.1:5000 to access the home page.


## 📁 Folder Structure

```text
<repository-name>/
├── app.py                  # Main Flask application file (routes for dashboard, etc.)
├── auth.py                 # Authentication module (signup, login, OTP, personal details)
├── resume_processing.py    # Functions for PDF text extraction, OCR, sorting resumes
├── requirements.txt        # Python dependencies
├── dataset/                # Folder containing resumes sorted by occupation
│   ├── Data Scientist/
│   └── Software Engineer/
├── uploads/                # Folder for user-uploaded files (e.g., ID proofs)
├── templates/              # HTML templates for Flask (base.html, index.html, etc.)
├── static/                 # Optional static assets (CSS, JS, images)
└── README.md               # Project documentation
```


## Additional Notes
1) Large Files:
If your resume dataset or other files exceed GitHub’s file size limit, consider using Git LFS to track large files.
2) Advanced NLP:
Replace simple regex extractions with libraries like spaCy or transformers for more robust resume parsing.
