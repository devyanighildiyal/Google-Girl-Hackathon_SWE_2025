import os, re
import fitz
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

DATASET_FOLDER = "dataset"

def extract_text_from_pdf(file_path):
    extracted_text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            extracted_text += page.get_text()
        doc.close()
        if not extracted_text.strip() and pytesseract:
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        extracted_text = f"Error processing PDF: {str(e)}"
    return extracted_text

def extract_resume_details(file_path):
    text = extract_text_from_pdf(file_path)
    name_match = re.search(r'Name:\s*(.*)', text)
    candidate_name = name_match.group(1).strip() if name_match else os.path.basename(file_path)
    exp_match = re.search(r'(\d+)\s+years', text, re.IGNORECASE)
    years_experience = int(exp_match.group(1)) if exp_match else 0
    return {"name": candidate_name, "years_experience": years_experience, "file": os.path.basename(file_path)}

def get_occupations():
    if not os.path.exists(DATASET_FOLDER):
        return []
    return [d for d in os.listdir(DATASET_FOLDER) if os.path.isdir(os.path.join(DATASET_FOLDER, d))]

def process_resume_dataset(occupation):
    folder_path = os.path.join(DATASET_FOLDER, occupation)
    if not os.path.exists(folder_path):
        return []
    resumes = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            details = extract_resume_details(file_path)
            resumes.append(details)
    resumes_sorted = sorted(resumes, key=lambda x: x["years_experience"], reverse=True)
    return resumes_sorted
