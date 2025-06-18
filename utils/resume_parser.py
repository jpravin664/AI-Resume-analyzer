import re
import pdfplumber
import docx2txt
from datetime import datetime
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def parse_resume(file_path):
    extension = file_path.split('.')[-1].lower()
    if extension == 'pdf':
        text = parse_pdf(file_path)
    elif extension in ['docx', 'doc']:
        text = parse_docx(file_path)
    elif extension == 'txt':
        text = parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")
    return extract_resume_data(text)


def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def parse_docx(file_path):
    return docx2txt.process(file_path)


def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()


def extract_resume_data(text):
    text = re.sub(r'\s+', ' ', text).strip()

    name = extract_name(text)
    email = extract_pattern(text, r'[\w\.-]+@[\w\.-]+\.\w+')
    phone = extract_pattern(text, r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
    education = extract_section(text, ['education'], ['experience', 'skills'])
    experience = extract_section(text, ['experience'], ['education', 'skills'])
    skills = extract_skills(text)

    resume_data = {
        'full_text': text,
        'name': name,
        'email': email,
        'phone': phone,
        'education': education,
        'experience': experience,
        'skills': skills,
        'parsed_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return resume_data


def extract_name(text):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_pattern(text, pattern):
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_section(text, start_keywords, stop_keywords):
    pattern = '|'.join([re.escape(word) for word in start_keywords])
    stop_pattern = '|'.join([re.escape(word) for word in stop_keywords])
    section = re.search(f'({pattern})(.*?)(?={stop_pattern}|$)', text, re.IGNORECASE)
    if section:
        return section.group(2).strip()
    return ""


def extract_skills(text):
    skills_section = extract_section(text, ['skills'], ['education', 'experience'])
    skills = re.split(r'[,;\n•-]', skills_section)
    return [skill.strip() for skill in skills if skill.strip()]

