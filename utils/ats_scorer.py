def calculate_ats_score(resume_data):
    """
    Calculate ATS compatibility score for a resume
    """
    score = 0
    max_score = 100
    feedback = []
    
    # Check for presence of key elements
    if resume_data['name']:
        score += 10
    else:
        feedback.append("Missing clear name at the top of resume")
    
    if resume_data['email']:
        score += 10
        if '@gmail.com' in resume_data['email'] or '@outlook.com' in resume_data['email'] or '@yahoo.com' in resume_data['email']:
            score += 5
            feedback.append("Professional email format detected")
        else:
            feedback.append("Consider using a professional email address")
    else:
        feedback.append("Missing email contact information")
    
    if resume_data['phone']:
        score += 10
    else:
        feedback.append("Missing phone contact information")
    
    if resume_data['education']:
        score += 15
        education_length = len(resume_data['education'])
        if education_length > 100:
            score += 5
            feedback.append("Good education section with details")
        else:
            feedback.append("Education section could use more details")
    else:
        feedback.append("Missing education information")
    
    if resume_data['experience']:
        score += 20
        experience_length = len(resume_data['experience'])
        if experience_length > 200:
            score += 10
            feedback.append("Detailed work experience section")
        else:
            feedback.append("Work experience section needs more details with accomplishments")
    else:
        feedback.append("Missing work experience section")
    
    if resume_data['skills'] and len(resume_data['skills']) >= 5:
        score += 15
        if len(resume_data['skills']) >= 10:
            score += 5
            feedback.append("Strong skills section with diverse abilities")
        else:
            feedback.append("Good skills section, but could include more relevant skills")
    else:
        feedback.append("Skills section needs improvement. Include at least 5-10 relevant skills")
    
    # Check for text length (a proxy for detail)
    full_text_length = len(resume_data['full_text'])
    if full_text_length > 2000:
        score += 5
        feedback.append("Good resume length with sufficient details")
    elif full_text_length < 1000:
        feedback.append("Resume may be too short. Add more details about your experience and skills")
    
    # Format score to integer
    final_score = min(max(int(score), 0), 100)
    
    # Add overall feedback based on score ranges
    if final_score >= 90:
        feedback.insert(0, "Excellent ATS-optimized resume!")
    elif final_score >= 75:
        feedback.insert(0, "Good ATS-compatible resume with some room for improvement")
    elif final_score >= 50:
        feedback.insert(0, "Average ATS compatibility. Follow the suggestions to improve your score")
    else:
        feedback.insert(0, "Your resume needs significant improvements for ATS compatibility")
    
    return final_score, feedback
