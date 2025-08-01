# === Smart Resume Analyzer & Job Matcher (ML Code) ===

# === ml_service/app.py ===
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
import re
import json
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

nlp = spacy.load('en_core_web_sm')
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Job Descriptions from JSON
with open('jobs.json') as f:
    job_descriptions = json.load(f)

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)
    resume_data = parse_resume(filepath)
    return jsonify(resume_data)

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    data = request.get_json()
    resume_text = data['resume_text']
    resume_embedding = bert_model.encode(resume_text, convert_to_tensor=True)

    matches = []
    for job in job_descriptions:
        job_text = job['description']
        job_embedding = bert_model.encode(job_text, convert_to_tensor=True)
        similarity = util.cos_sim(resume_embedding, job_embedding).item()
        matches.append({
            'title': job['title'],
            'description': job_text,
            'similarity': round(similarity * 100, 2)
        })

    matches = sorted(matches, key=lambda x: x['similarity'], reverse=True)
    return jsonify({'matches': matches[:5]})

@app.route('/suggest-improvements', methods=['POST'])
def suggest_improvements():
    data = request.get_json()
    resume_text = data['resume_text']
    target_job_text = data['job_text']

    resume_tokens = set([token.text.lower() for token in nlp(resume_text) if token.is_alpha])
    job_tokens = set([token.text.lower() for token in nlp(target_job_text) if token.is_alpha])
    missing_keywords = list(job_tokens - resume_tokens)

    return jsonify({'missing_keywords': missing_keywords[:20]})

def parse_resume(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()

    name = extract_name(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    return {
        "name": name,
        "skills": skills,
        "education": education,
        "experience": experience,
        "resume_text": text
    }

def extract_name(text):
    lines = text.split('\n')
    return lines[0].strip() if lines else ""

def extract_skills(text):
    skills = re.findall(r"\b(JavaScript|Python|Java|SQL|React|Node|AWS|Machine Learning|Data Analysis)\b", text, re.I)
    return list(set(skills))

def extract_education(text):
    edu_keywords = ['bachelor', 'master', 'b.sc', 'm.sc', 'b.tech', 'm.tech', 'phd']
    found = [line for line in text.lower().split('\n') if any(k in line for k in edu_keywords)]
    return found

def extract_experience(text):
    exp_lines = [line for line in text.split('\n') if re.search(r'\d+\s+years?', line, re.I)]
    return exp_lines

if __name__ == '__main__':
    app.run(debug=True, port=5001)