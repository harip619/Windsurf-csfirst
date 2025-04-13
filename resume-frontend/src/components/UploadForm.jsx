import React, { useState } from 'react';
import axios from 'axios';
import ResumeSummary from './ResumeSummary';

// Use the same API URL as ResumeHistory
const API_URL = '/api';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a PDF file!");
      return;
    }
    
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      
      console.log('Upload response:', res.data);
      // Extract the data field from the response
      setResult(res.data.data);
    } catch (err) {
      console.error('Upload failed:', err);
      setError(err.response?.data?.error || "Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4">
        <h2 className="text-center mb-4">Resume Skill Extractor</h2>

        <div className="mb-3">
          <input
            className="form-control"
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            disabled={loading}
          />
        </div>

        {error && (
          <div className="alert alert-danger mb-3">
            {error}
          </div>
        )}

        <div className="d-grid">
          <button 
            className="btn btn-primary" 
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? 'Processing...' : 'Upload Resume'}
          </button>
        </div>

        {result && (
          <div className="mt-5">
            <h4 className="mb-3">Extracted Information</h4>
            <ResumeSummary data={result} />
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadForm;
