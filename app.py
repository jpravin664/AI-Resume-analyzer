from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import tempfile
from utils.resume_parser import parse_resume
from utils.ats_scorer import calculate_ats_score
from utils.job_matcher import calculate_job_match

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    resume_file = request.files['resume']
    if resume_file.filename == '':
        return jsonify({'error': 'No resume file selected'}), 400
    
    if not allowed_file(resume_file.filename):
        return jsonify({'error': f'File type not allowed. Please upload {", ".join(ALLOWED_EXTENSIONS)}'}, 400)
    
    # Save the resume to a temporary file
    resume_filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    resume_file.save(resume_path)
    
    # Parse the resume
    try:
        resume_data = parse_resume(resume_path)
    except Exception as e:
        os.remove(resume_path)
        return jsonify({'error': f'Error parsing resume: {str(e)}'}), 500
    
    # Calculate ATS score
    ats_score, ats_feedback = calculate_ats_score(resume_data)
    
    # Check if job description is provided
    job_match = None
    job_match_feedback = None
    if 'job_description' in request.form and request.form['job_description'].strip():
        job_description = request.form['job_description']
        job_match, job_match_feedback = calculate_job_match(resume_data, job_description)
    
    # Clean up the temporary file
    os.remove(resume_path)
    
    # Prepare response
    result = {
        'ats_score': ats_score,
        'ats_feedback': ats_feedback,
        'resume_data': resume_data,
    }
    
    if job_match is not None:
        result['job_match'] = job_match
        result['job_match_feedback'] = job_match_feedback
    
    return render_template('results.html', result=result)

if __name__ == '__main__':
    os.makedirs('utils', exist_ok=True)
    app.run(debug=True)
