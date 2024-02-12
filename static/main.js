function extractPDF() {
    const input = document.getElementById('pdfInput');
    const output = document.getElementById('output');

    const file = input.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('pdf', file);

        fetch('/extract', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                output.textContent = data.text;
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select a PDF file.');
    }
}
