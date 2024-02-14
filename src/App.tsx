import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { CvForm } from './CvForm';
import './App.css';

interface CvData {
  personalInformation: {
    name: string;
    address: string;
    phone: string;
    email: string;
  };
  education: {
    degree: string;
    lastAttended: string;
    university: string;
  };
}

export const PdfExtractor: React.FC = () => {
  const [cvData, setCvData] = useState<CvData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [populate, setPopulate] = useState(false );

  const onDrop = async (acceptedFiles: File[]) => {
    const pdfFile = acceptedFiles[0];

    const formData = new FormData();
    formData.append('pdf', pdfFile);

    try {
      setLoading(true);

      const response = await axios.post('http://127.0.0.1:5000/extract', formData);
      const { success, cvData, error } = response.data;

      if (success) {
        setCvData(cvData);
        setError(null);
      } else {
        setCvData(null);
        setError(error || 'An error occurred while processing the PDF.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('An error occurred while uploading or processing the PDF.');
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: false,
  });

  const handlePopulate = () => {
    setPopulate(true);
  }

  return (
    <div className="pdf-extractor-container">
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        <p className="dropzone-text">{loading ? 'Processing...' : 'Drag & drop a PDF file here, or click to select one'}</p>
      </div>

      {cvData && (
        <div className="extracted-data-container">
          <h2>Extracted CV Data:</h2>
          <pre className="extracted-data">{JSON.stringify(cvData, null, 2)}</pre>
          <button onClick={handlePopulate} className="upload-button">
            Upload
          </button>
        </div>
      )}

      {cvData && populate && (
        <CvForm
          education={cvData.education}
          personalInformation={cvData.personalInformation}
        />
      )}

      {error && <p className="error-message">{error}</p>}
    </div>
  );
};
