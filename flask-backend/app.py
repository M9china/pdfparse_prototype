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
    education_pattern = re.compile(r'Education\s*\n•\s*([^•]+?) - (.+), Graduated (.+)\no Relevant Coursework: (.+)')
    match_education = education_pattern.search(text)
    if match_education:
        cv_data["education"]["degree"] = match_education.group(1).strip()
        cv_data["education"]["institution"] = match_education.group(2).strip()
        cv_data["education"]["graduationDate"] = match_education.group(3).strip()
        cv_data["education"]["relevantCoursework"] = [course.strip() for course in match_education.group(4).split(',')]


    # Experience information
    experience_pattern = re.compile(r'Experience\s*\n([^•]+) - (.+), (.+) \((.+) - (.+)\)\n• (.+)')
    match_experience = experience_pattern.search(text)

    if match_experience:
        cv_data["experience"] = {
            "title": match_experience.group(1).strip(),
            "company": match_experience.group(2).strip(),
            "location": match_experience.group(3).strip(),
            "duration": f"{match_experience.group(4)} - {match_experience.group(5)}",
            "responsibilities": [responsibility.strip() for responsibility in match_experience.group(6).split('•')]
        }

    # Skills information
    skills_pattern = re.compile(r'Skills\s*\n•\s*Technical Skills: (.+)\n•\s*Soft Skills: (.+)')
    match_skills = skills_pattern.search(text)

    if match_skills:
        cv_data["skills"]["technicalSkills"] = [skill.strip() for skill in match_skills.group(1).split(',')]
        cv_data["skills"]["softSkills"] = [skill.strip() for skill in match_skills.group(2).split(',')]


    # Certifications information
    certifications_pattern = re.compile(r'Certifications\s*\n•\s*([^•]+?)\s*-\s*([^,]+),\s*(\d{4})')
    match_certifications = certifications_pattern.findall(text)

    if match_certifications:
        cv_data["certifications"] = [
            {
                "title": entry[0].strip(),
                "issuer": entry[1].strip(),
                "year": entry[2]
            }
            for entry in match_certifications
        ]



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
    volunteer_pattern = re.compile(r'Volunteer Experience \s*\n•\s*([^•]+?) - (.+), Volunteer Web Developer (.+)\no Developed a volunteer management web application (.+)')
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
