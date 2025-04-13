import PyPDF2
import re
import spacy
from spacy.matcher import Matcher
import logging

logger = logging.getLogger(__name__)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        logger.debug(f"Extracted text: {text[:500]}...")  # Log first 500 chars
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_email(text):
    # Fix common email formatting issues
    text = text.replace('\n@', '@').replace('.\n', '')
    text = text.replace(' @ ', '@')  # Fix spaced @ symbol
    text = text.replace(' . ', '.')  # Fix spaced dots
    text = re.sub(r'\s+@\s+', '@', text)  # Fix any whitespace around @
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(email_pattern, text)

    if not emails:
        logger.debug("No email found.")
        return ""

    # List of preferred email patterns (in order of priority)
    preferred_patterns = [
        "haripradeep",
        "hari",
        "radeep",
        # Add more patterns here if needed
    ]

    # First try: Look for preferred patterns
    for pattern in preferred_patterns:
        for email in emails:
            if email.lower().startswith(pattern):
                logger.debug(f"Found preferred email ({pattern}): {email}")
                return email

    # Second try: Look for personal email domains
    personal_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    for email in emails:
        domain = email.lower().split('@')[1]
        if domain in personal_domains:
            logger.debug(f"Found personal email: {email}")
            return email

    # Fallback: Use the first email found
    logger.debug(f"Using default email: {emails[0]}")
    return emails[0]

def extract_phone(text):
    # Clean up the text
    text = text.replace('\n', ' ')  # Fix split phone numbers
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    # Common phone number patterns
    phone_patterns = [
        r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # International: +1-234-567-8900
        r'\(\+\d{1,3}\)\s*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # International: (+1) 234-567-8900
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',                  # US/Local: 234-567-8900
        r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',                  # US/Local: (234) 567-8900
        r'\d{10}',                                          # Plain: 2345678900
        r'\d{3}[-.\s]?\d{4}[-.\s]?\d{3}'                   # Alternate: 234-4567-890
    ]
    
    # Try each pattern
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            # Clean up the found number
            number = phones[0]
            # Remove all non-digit characters except + for international
            cleaned = re.sub(r'[^\d+]', '', number)
            logger.debug(f"Found phone number: {number} -> cleaned: {cleaned}")
            return cleaned
            
    logger.debug("No phone number found")
    return ""

def extract_name(text):
    # Use NLP on the first few lines
    lines = text.strip().split('\n')
    first_lines = " ".join(lines[:5])
    doc = nlp(first_lines)

    # First try: Named Entity Recognition
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            logger.debug(f"Extracted name using NLP: {ent.text}")
            return ent.text

    # Fallback: Heuristically guess name from first lines
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[A-Z][A-Z ]{1,40}$', line) and "RESUME" not in line:
            logger.debug(f"Extracted name heuristically: {line.title()}")
            return line.title()

    # Final fallback: first non-empty line
    first_non_empty = next((l for l in lines if l.strip()), "")
    logger.debug(f"Using fallback first line as name: {first_non_empty}")
    return first_non_empty

def extract_skills(text):
    # Comprehensive list of technical skills
    technical_skills = {
        # Programming Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go",
        # Web Technologies
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "jQuery", "Bootstrap", "Sass", "REST API", "GraphQL", "WebSocket",
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite", "NoSQL",
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", "CI/CD", "Linux",
        "Terraform", "Ansible", "Nginx", "Apache",
        # Data Science & AI
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "NLP",
        "Computer Vision", "Data Analysis", "Neural Networks", "AI",
        # Mobile Development
        "Android", "iOS", "React Native", "Flutter", "Mobile Development",
        # Other Technologies
        "Agile", "Scrum", "RESTful", "Microservices", "System Design", "OOP", "Design Patterns"
    }
    
    # Clean up text
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    # Find skills
    found_skills = set()
    
    # Direct matching
    for skill in technical_skills:
        # Handle variations (e.g., "reactjs" matches "react")
        skill_pattern = skill.lower().replace('.', r'\.?').replace('+', r'\+?').replace('#', r'#?')
        if re.search(rf'\b{skill_pattern}(?:js)?\b', text):
            found_skills.add(skill)
    
    # Sort skills alphabetically for consistent output
    skills_list = sorted(list(found_skills))
    
    logger.debug(f"Found {len(skills_list)} skills: {skills_list}")
    return skills_list

def extract_work_experience(text):
    # Keywords that typically indicate work experience sections
    work_markers = [
        "EXPERIENCE", "EMPLOYMENT", "WORK HISTORY", "PROFESSIONAL BACKGROUND",
        "PROFESSIONAL EXPERIENCE", "CAREER HISTORY"
    ]
    
    lines = text.split('\n')
    experience = []
    capturing = False
    
    for i, line in enumerate(lines):
        # Check if this line contains a work experience marker
        if any(marker in line.upper() for marker in work_markers):
            capturing = True
            logger.debug(f"Found work experience marker: {line}")
            continue
            
        # Stop capturing if we hit another major section
        if capturing and line.strip().isupper() and len(line.strip()) > 10:
            break
            
        # Add non-empty lines while capturing
        if capturing and line.strip():
            experience.append(line.strip())
            
        # Limit to first 5 entries
        if len(experience) >= 5:
            break
    
    logger.debug(f"Extracted work experience: {experience}")
    return experience if experience else []

def extract_resume_data(file_path):
    logger.info(f"Starting resume extraction from: {file_path}")
    
    # Extract text from PDF
    text = extract_text_from_pdf(file_path)
    if not text:
        logger.error("No text extracted from PDF")
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "work_experience": []
        }
    
    # Extract individual components
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    work_experience = extract_work_experience(text)
    
    result = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "work_experience": work_experience
    }
    
    logger.info("Extraction complete")
    logger.debug(f"Final extracted data: {result}")
    return result
