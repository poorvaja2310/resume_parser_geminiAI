# """
# Configuration settings for the Resume Parser System
# """

# import os
# from pathlib import Path

# # Directory settings
# BASE_DIR = Path(__file__).parent
# DATA_DIR = BASE_DIR / "data"
# RESUMES_DIR = DATA_DIR / "resumes"
# JSON_DIR = DATA_DIR / "parsed_resumes"

# # Create directories if they don't exist
# DATA_DIR.mkdir(exist_ok=True)
# RESUMES_DIR.mkdir(exist_ok=True)
# JSON_DIR.mkdir(exist_ok=True)

# # File settings
# ALLOWED_EXTENSIONS = ['.pdf', '.docx']
# MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# # Gemini AI settings
# GEMINI_MODEL = "gemini-pro"
# GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

# # Direct API key configuration (optional)
# # Replace 'your-api-key-here' with your actual Gemini API key
# GEMINI_API_KEY_DIRECT = "AIzaSyBvPYBsaBOxSSWnjFAK956qIo7Xo3iZwJE"  # Insert your API key here

# # Parsing settings
# SKILLS_KEYWORDS = [
#     'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb', 
#     'aws', 'docker', 'kubernetes', 'machine learning', 'data science',
#     'html', 'css', 'typescript', 'angular', 'vue.js', 'postgresql',
#     'redis', 'elasticsearch', 'git', 'agile', 'scrum', 'tensorflow',
#     'pytorch', 'scikit-learn', 'pandas', 'numpy', 'flask', 'django',
#     'fastapi', 'spring boot', 'microservices', 'rest api', 'graphql'
# ]

# EDUCATION_KEYWORDS = [
#     'bachelor', 'master', 'phd', 'doctorate', 'degree', 'university',
#     'college', 'institute', 'certification', 'diploma', 'b.tech',
#     'm.tech', 'mba', 'bca', 'mca', 'be', 'me', 'ms', 'bs'
# ]

"""
Configuration settings for the Resume Parser System
"""

import os
from pathlib import Path

# Directory settings (for temporary operations if needed)
BASE_DIR = Path(__file__).parent

# File settings
ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.txt']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Gemini AI settings
GEMINI_MODEL = "gemini-pro"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

# Direct API key configuration (optional)
# Replace with your actual Gemini API key
GEMINI_API_KEY_DIRECT = "AIzaSyBvPYBsaBOxSSWnjFAK956qIo7Xo3iZwJE"  # Insert your API key here

# Parsing settings
DEFAULT_PARSING_PROMPT = """
Extract the following information from this resume in JSON format with these exact field names:
- name: Full name of the candidate (required)
- email: Email address
- phone: Phone number
- experience_years: Total years of work experience (as a number)
- skills: List of technical/professional skills
- education: List of educational qualifications
- summary: Brief professional summary (2-3 sentences)

IMPORTANT: 
1. For the name field, carefully extract the candidate's full name from the resume. 
2. If you cannot find a name, use "Unknown Candidate" as the value.
3. Return ONLY valid JSON with these exact field names. 
4. Do not include any additional text or explanations outside the JSON.

Example format:
{
  "name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "+1-555-123-4567",
  "experience_years": 5,
  "skills": ["Python", "JavaScript", "SQL"],
  "education": ["Bachelor of Science in Computer Science"],
  "summary": "Experienced software developer with 5 years of expertise in web development..."
}
"""