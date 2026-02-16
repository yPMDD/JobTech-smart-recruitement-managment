import re
import spacy
import PyPDF2
import docx
from collections import defaultdict

# Global variable for the model
nlp = None

def load_spacy_model():
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading 'en_core_web_sm' model...")
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX files"""
    text = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_resume_sections(text):
    """Extract skills, education, and experience from resume text"""
    # Initialize results dictionary
    results = {
        'skills': set(),
        'education': [],
        'experience': []
    }
    
    # Convert to lowercase for case-insensitive matching
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Load model (lazy loading)
    nlp = load_spacy_model()
    doc = nlp(text_lower)
    
    # SECTION 1: SKILLS EXTRACTION
    # Common skill keywords (expand this list)
    skill_keywords = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby'],
        'web': ['html', 'css', 'django', 'flask', 'react', 'angular', 'vue'],
        'databases': ['mysql', 'postgresql', 'mongodb', 'sql', 'oracle'],
        'devops': ['docker', 'kubernetes', 'aws', 'azure', 'ci/cd']
    }
    
    # Flatten all skills into one list
    all_skills = [skill for sublist in skill_keywords.values() for skill in sublist]
    
    # Extract from explicit skills section
    skills_section = extract_section(text, 'skills|technical skills|competencies')
    if skills_section:
        for token in nlp(skills_section):
            if token.text.lower() in all_skills:
                results['skills'].add(token.text.lower())
    
    # Extract skills from entire document as fallback
    for token in doc:
        if token.text.lower() in all_skills:
            results['skills'].add(token.text.lower())
    
    

    # SECTION 2: EDUCATION EXTRACTION
    education_section = extract_section(text, 'education|academic background|degrees|EDUCATION')
    if education_section:
        results['education'] = process_education(education_section)
    
    # SECTION 3: EXPERIENCE EXTRACTION
    experience_section = extract_section(text, 'experience|work history|employment|PROJETS REALISÉS')
    if experience_section:
        results['experience'] = process_experience(experience_section)
    
    # Convert skills set to list
    results['skills'] = list(results['skills'])
    
    return results

def extract_section(text, section_pattern):
    """Extract a specific section from resume text"""
    match = re.search(fr'({section_pattern}).*?$', text, re.IGNORECASE | re.MULTILINE)
    if match:
        section_start = match.end()
        # Find the end of the section (next section or end of document)
        next_section = re.search(r'\n\s*(education|experience|skills|projects|$)', 
                                text[section_start:], re.IGNORECASE)
        end_pos = section_start + (next_section.start() if next_section else len(text))
        return text[section_start:end_pos].strip()
    return None

def process_education(education_text):
    """Process and clean education section"""
    education_items = []
    for line in education_text.split('\n'):
        line = line.strip()
        if line and len(line) > 10:  # Basic filter for meaningful lines
            # Remove dates, GPAs, etc. (simplified)
            line = re.sub(r'\(.*?\)|\[.*?\]|\b\d{4}\b', '', line).strip()
            if line:
                education_items.append(line)
    return education_items[:3]  # Return top 3 education items

def process_experience(experience_text):
    """Process and clean experience section"""
    experience_items = []
    for line in experience_text.split('\n'):
        line = line.strip()
        if line and len(line) > 10:  # Basic filter for meaningful lines
            # Remove dates, locations (simplified)
            line = re.sub(r'\(.*?\)|\[.*?\]|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}\b', '', line).strip()
            if line:
                experience_items.append(line)
    return experience_items[:3]  # Return top 3 experience items