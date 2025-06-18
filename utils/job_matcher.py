import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_job_match(resume_data, job_description):
    """
    Calculate job match score between resume and job description
    """
    # Combine all resume text
    resume_text = resume_data['full_text']
    
    # Prepare the texts
    documents = [resume_text, job_description]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Convert to percentage score
    match_score = int(cosine_sim * 100)
    
    # Extract key skills from job description
    job_skills = extract_skills_from_text(job_description)
    resume_skills = resume_data['skills']
    
    # Calculate skill match
    matching_skills = []
    missing_skills = []
    
    for skill in job_skills:
        skill_lower = skill.lower()
        found = False
        for resume_skill in resume_skills:
            if skill_lower in resume_skill.lower():
                matching_skills.append(skill)
                found = True
                break
        if not found:
            missing_skills.append(skill)
    
    skill_match_percentage = 0
    if job_skills:
        skill_match_percentage = int((len(matching_skills) / len(job_skills)) * 100)
    
    # Final combined score (60% content match, 40% skill match)
    final_score = int(match_score * 0.6 + skill_match_percentage * 0.4)
    
    # Prepare feedback
    feedback = []
    
    if final_score >= 80:
        feedback.append("Strong match! Your resume aligns well with this job description.")
    elif final_score >= 60:
        feedback.append("Good match. With some adjustments, your resume could be an excellent fit.")
    elif final_score >= 40:
        feedback.append("Moderate match. Consider tailoring your resume further to this position.")
    else:
        feedback.append("Low match. Your resume needs significant adjustments to align with this job.")
    
    # Add specific feedback
    if matching_skills:
        feedback.append(f"Matching skills: {', '.join(matching_skills[:5])}{' and more' if len(matching_skills) > 5 else ''}")
    
    if missing_skills:
        top_missing = missing_skills[:5]
        feedback.append(f"Missing key skills: {', '.join(top_missing)}{' and more' if len(missing_skills) > 5 else ''}")
        feedback.append("Consider adding these skills to your resume if you have them.")
    
    # Keyword density analysis
    keywords = extract_keywords_from_job_description(job_description)
    keyword_feedback = analyze_keyword_density(resume_text, keywords)
    feedback.extend(keyword_feedback)
    
    return final_score, feedback

def extract_skills_from_text(text):
    """
    Extract potential skills from text using common patterns
    """
    # List of common technical skills and keywords
    common_skills = [
        "Python", "Java", "JavaScript", "C++", "SQL", "Excel", "PowerPoint",
        "Project Management", "Leadership", "Communication", "Analysis", "Research",
        "Marketing", "Sales", "Customer Service", "Data Analysis", "Machine Learning",
        "AI", "Artificial Intelligence", "Cloud", "AWS", "Azure", "GCP", "DevOps",
        "Agile", "Scrum", "Kanban", "Django", "Flask", "React", "Angular", "Vue",
        "Node.js", "Express", "MongoDB", "MySQL", "PostgreSQL", "Oracle", "NoSQL",
        "Docker", "Kubernetes", "Terraform", "CI/CD", "Git", "GitHub", "Jira",
        "HTML", "CSS", "PHP", "Ruby", "Swift", "Kotlin", "Go", "Rust", "Scala",
        "Microsoft Office", "Tableau", "Power BI", "Adobe", "Photoshop", "Illustrator",
        "InDesign", "Figma", "Sketch", "UI/UX", "SEO", "SEM", "Content Writing",
        "Social Media", "Analytics", "Team Management", "Budget Management", "Strategy",
        "Planning", "Execution", "Problem Solving", "Critical Thinking", "Time Management",

        # Cyber Security Skills
        "Cyber Security", "Information Security", "Network Security", "Endpoint Security",
        "Threat Detection", "Vulnerability Assessment", "Penetration Testing", "Ethical Hacking",
        "Security Auditing", "Incident Response", "Security Analysis", "SIEM", "IDS/IPS",
        "Firewalls", "Cryptography", "Malware Analysis", "Reverse Engineering",
        "Risk Management", "Compliance", "GDPR", "HIPAA", "ISO 27001", "Security Architecture",
        "Cloud Security", "IAM", "Access Control", "Security Engineering", "Security Operations",

        # AI and Machine Learning Skills (Expanding)
        "Deep Learning", "Natural Language Processing (NLP)", "Computer Vision",
        "Reinforcement Learning", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
        "Data Mining", "Feature Engineering", "Model Deployment", "Statistical Modeling",
        "Time Series Analysis", "Big Data", "Hadoop", "Spark", "Data Visualization",
        "Predictive Modeling", "Generative AI", "LLMs", "Transformer Networks",

        # Web Development Skills (Expanding)
        "Front-end Development", "Back-end Development", "Full-stack Development",
        "Responsive Design", "Mobile-First Design", "RESTful APIs", "GraphQL",
        "Web Services", "API Development", "Database Design", "ORM", "Server-side Rendering",
        "Client-side Rendering", "State Management", "Redux", "Context API",
        "Testing (Unit, Integration, E2E)", "Web Security", "Performance Optimization",
        "JAMstack", "Serverless", "CMS (Content Management Systems)", "WordPress", "Drupal",
        "Headless CMS"
    ]
    
    # Create regex pattern for skill extraction
    skill_pattern = r'\b(?:' + '|'.join(common_skills) + r')\b'
    skills = re.findall(skill_pattern, text, re.IGNORECASE)
    
    # Remove duplicates and normalize
    unique_skills = list(set([skill.strip() for skill in skills]))
    
    return unique_skills

def extract_keywords_from_job_description(job_description):
    """
    Extract important keywords from job description
    """
    # Remove common stop words
    stop_words = ["a", "an", "the", "and", "or", "but", "is", "are", "in", "to", "for", "with", "on", "at", "by", "of"]
    words = job_description.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    
    # Count word frequency
    word_freq = {}
    for word in filtered_words:
        if len(word) > 3:  # Only consider words with length > 3
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Return top 15 keywords
    return [word for word, freq in sorted_keywords[:15]]

def analyze_keyword_density(resume_text, keywords):
    """
    Analyze keyword density in resume
    """
    feedback = []
    resume_text_lower = resume_text.lower()
    missing_keywords = []
    low_frequency_keywords = []
    
    for keyword in keywords:
        count = resume_text_lower.count(keyword.lower())
        if count == 0:
            missing_keywords.append(keyword)
        elif count < 2:
            low_frequency_keywords.append(keyword)
    
    if missing_keywords:
        top_missing = missing_keywords[:5]
        feedback.append(f"Consider adding these important keywords: {', '.join(top_missing)}{' and more' if len(missing_keywords) > 5 else ''}")
    
    if low_frequency_keywords:
        top_low_freq = low_frequency_keywords[:3]
        feedback.append(f"These keywords appear infrequently: {', '.join(top_low_freq)}. Consider emphasizing them more.")
    
    return feedback