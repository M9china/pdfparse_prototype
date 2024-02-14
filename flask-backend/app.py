import io
import re
from flask import Flask, render_template, request, jsonify
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Structure (template)
cv_template = {
    "personalInformation": {

    },
    "objective": "",
    "education": {
        "degree": "",
        "institution": "",
        "graduationDate": "",
        "relevantCoursework": []
    },
    "experience": [
        {
            "title": "",
            "company": "",
            "location": "",
            "duration": "",
            "responsibilities": []
        }
    ],
    "skills": {
        "technicalSkills": [],
        "softSkills": []
    },
    "certifications": [
        {
            "title": "",
            "issuer": "",
            "year": ""
        }
    ],
    "projects": [
        {
            "name": "",
            "duration": "",
            "description": "",
            "technologies": []
        }
    ],
    "volunteerExperience": [
        {
            "title": "",
            "organization": "",
            "location": "",
            "duration": "",
            "responsibilities": []
        }
    ],
    "interests": [],
    "references": ""
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    try:
        pdf_file = request.files['pdf']

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            cv_data = process_cv(pdf_file)
            return jsonify({'success': True, 'cvData': cv_data})
        else:
            return jsonify({'success': False, 'error': 'Invalid PDF file.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def process_cv(pdf_file):
    cv_data = cv_template.copy()

    pdf_content = pdf_file.read()

    with io.BytesIO(pdf_content) as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

    # Personal information
    personal_info_pattern = re.compile(r'([^•]+)\n• Address: ([^•]+)\n• Phone: ([^•]+)\n• Email: ([^•]+)\n• LinkedIn: (.+)')
    match_personal_info = personal_info_pattern.search(text)
    if match_personal_info:
        cv_data["personalInformation"]["name"] = match_personal_info.group(1).strip()
        cv_data["personalInformation"]["address"] = match_personal_info.group(2).strip()
        cv_data["personalInformation"]["phone"] = match_personal_info.group(3).strip()
        cv_data["personalInformation"]["email"] = match_personal_info.group(4).strip()
        cv_data["personalInformation"]["linkedIn"] = match_personal_info.group(5).strip()



    # Education information
    education_pattern = re.compile(r'Bachelor of Science in Computer Science - (.+), Graduated (.+)\no Relevant Coursework: (.+)')
    match_education = education_pattern.search(text)
    if match_education:
        cv_data["education"]["degree"] = "Bachelor of Science in Computer Science"
        cv_data["education"]["institution"] = match_education.group(1)
        cv_data["education"]["graduationDate"] = match_education.group(2)
        cv_data["education"]["relevantCoursework"] = [course.strip() for course in match_education.group(3).split(',')]

    # Experience information
    experience_pattern = re.compile(r'([^•]+) - (.+), (.+) \((.+) - (.+)\)\n• (.+)')
    match_experience = experience_pattern.findall(text)
    if match_experience:
        cv_data["experience"] = [
            {
                "title": entry[0],
                "company": entry[1],
                "location": entry[2],
                "duration": f"{entry[3]} - {entry[4]}",
                "responsibilities": [responsibility.strip() for responsibility in entry[5].split('•')]
            }
            for entry in match_experience
        ]

    # Technical skills
    technical_skills_pattern = re.compile(r'Technical Skills\n• Technical Skills: (.+)\n• Soft Skills: (.+)')
    match_technical_skills = technical_skills_pattern.search(text)
    if match_technical_skills:
        cv_data["skills"]["technicalSkills"] = [skill.strip() for skill in match_technical_skills.group(1).split(',')]
        cv_data["skills"]["softSkills"] = [skill.strip() for skill in match_technical_skills.group(2).split(',')]

    # Certifications information
    certifications_pattern = re.compile(r'Certified Full Stack Web Developer - (.+), (\d{4})')
    match_certifications = certifications_pattern.search(text)
    if match_certifications:
        cv_data["certifications"] = {
            "title": "Certified Full Stack Web Developer",
            "issuer": match_certifications.group(1),
            "year": match_certifications.group(2)
        }

    # Projects information
    projects_pattern = re.compile(r'(.+) \((.+ - .+)\)\n• (.+)\n• Technologies used: (.+)')
    match_projects = projects_pattern.findall(text)
    if match_projects:
        cv_data["projects"] = [
            {
                "name": entry[0],
                "duration": entry[1],
                "description": entry[2],
                "technologies": [tech.strip() for tech in entry[3].split(',')]
            }
            for entry in match_projects
        ]

    # Volunteer experience information
    volunteer_pattern = re.compile(r'Volunteer Web Developer - (.+), (.+) \((.+) - (.+)\)\no (.+)')
    match_volunteer = volunteer_pattern.findall(text)
    if match_volunteer:
        cv_data["volunteerExperience"] = [
            {
                "title": entry[0],
                "organization": entry[1],
                "location": entry[2],
                "duration": f"{entry[3]} - {entry[4]}",
                "responsibilities": [responsibility.strip() for responsibility in entry[5].split('o')]
            }
            for entry in match_volunteer
        ]

    # Interests information
    interests_pattern = re.compile(r'Interests\n• (.+)')
    match_interests = interests_pattern.search(text)
    if match_interests:
        cv_data["interests"] = [interest.strip() for interest in match_interests.group(1).split(',')]

    # References information
    references_pattern = re.compile(r'References\n• (.+)')
    match_references = references_pattern.search(text)
    if match_references:
        cv_data["references"] = match_references.group(1).strip()

    return cv_data

if __name__ == '__main__':
    app.run(debug=True)
