import React from 'react';
import './App.css';

interface CvFormProps {
  education: {
    degree: string;
    graduationDate: string;
    institution: string;
  };
  personalInformation: {
    address: string;
    email: string;
    name: string;
    phone: string;
  };
}

export const CvForm: React.FC<CvFormProps> = ({ education, personalInformation }) => {
  return (
    <div className="cv-form-container">
      <form className="cv-form">
        <div className="section">
          <h2>Education</h2>
          <div className="form-group">
            <label>Qualification:</label>
            <input type="text" value={education.degree} readOnly />
          </div>
          <div className="form-group">
            <label>Graduated:</label>
            <input type="text" value={education.graduationDate} readOnly />
          </div>
          <div className="form-group">
            <label>University:</label>
            <input type="text" value={education.institution} readOnly />
          </div>
        </div>

        <div className="section">
          <h2>Personal Information</h2>
          <div className="form-group">
            <label>Name:</label>
            <input type="text" value={personalInformation.name} readOnly />
          </div>
          <div className="form-group">
            <label>Address:</label>
            <input type="text" value={personalInformation.address} readOnly />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input type="text" value={personalInformation.email} readOnly />
          </div>
          <div className="form-group">
            <label>Phone:</label>
            <input type="text" value={personalInformation.phone} readOnly />
          </div>
        </div>
      </form>
    </div>
  );
};