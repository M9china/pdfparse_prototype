import io
import re
from flask import Flask, render_template, request, jsonify
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# structure (template)
cv_template = {
    "personalInformation": {},
    "education": {
    },
    "technicalSkills": {
        "programmingLanguages": [],
        "webDevelopment": [],
        "database": [],
        "toolsAndTechnologies": [],
        "softwareEngineering": []
    },
    "projects": [],
    "professionalDevelopment": {
        "program": "",
        "enrollmentPeriod": "",
        "focus": ""
    },
    "extraCurricularActivities": [],
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

    # personal information
    personal_info_pattern = re.compile(r'([^|]+) \| ([^|]+, [^|]+) \| ([^|]+) \| ([^|\n]+)')
    match_personal_info = personal_info_pattern.search(text)
    if match_personal_info:
        cv_data["personalInformation"]["name"] = match_personal_info.group(1).replace('\n', ' ').strip()
        cv_data["personalInformation"]["address"] = match_personal_info.group(2).strip()
        cv_data["personalInformation"]["phone"] = match_personal_info.group(3).strip()
        cv_data["personalInformation"]["email"] = match_personal_info.group(4).strip()
    
    # education information
    education_pattern = re.compile(r'Education\n• (.+), (.+)\n(.+)\n(.+)')
    match_education = education_pattern.search(text)
    if match_education:
        cv_data["education"]["university"] = match_education.group(1)
        cv_data["education"]["degree"] = match_education.group(2)
        cv_data["education"]["lastAttended"] = match_education.group(4)

    # technical skills
    technical_skills_pattern = re.compile(r'Technical Skills\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)\n• (.+)')
    match_technical_skills = technical_skills_pattern.search(text)
    if match_technical_skills:
        cv_data["technicalSkills"]["programmingLanguages"] = match_technical_skills.group(1, 2, 3, 4, 5)
        cv_data["technicalSkills"]["frameworks"] = [match_technical_skills.group(6)]
        cv_data["technicalSkills"]["styling"] = [match_technical_skills.group(7)]
        cv_data["technicalSkills"]["database"] = [match_technical_skills.group(8), match_technical_skills.group(9)]
        cv_data["technicalSkills"]["tools"] = [match_technical_skills.group(10)]
        cv_data["technicalSkills"]["versionControl"] = [match_technical_skills.group(11)]


    return cv_data



if __name__ == '__main__':
    app.run(debug=True)
