# HelperMS        
AI-Driven HR Platform: An intelligent HR platform prototype that automates tasks like resume screening, onboarding, interview scheduling, and more.

## Table of Contents: 
1) Project Overview
2) Key Features
3) Environment Setup
4) How to Run
5) Folder Structure
6) Additional Notes

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
