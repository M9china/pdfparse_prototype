from flask import Flask, render_template, request, jsonify
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    try:
        pdf_file = request.files['pdf']

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            return jsonify({'success': True, 'text': text})
        else:
            return jsonify({'success': False, 'error': 'Invalid PDF file.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
