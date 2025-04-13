import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ResumeSummary from './ResumeSummary';

// In Docker, we access the backend through nginx proxy
const API_URL = '/api';

function ResumeHistory() {
  const [resumes, setResumes] = useState([]);
  const [filteredResumes, setFilteredResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [availableSkills, setAvailableSkills] = useState(new Set());

  useEffect(() => {
    console.log('ResumeHistory component mounted');
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      console.log('Fetching resumes from:', `${API_URL}/resumes`);
      const response = await axios.get(`${API_URL}/resumes`);
      console.log('Raw response:', response);
      console.log('Response data:', JSON.stringify(response.data, null, 2));
      
      if (Array.isArray(response.data)) {
        console.log('Setting resumes:', response.data.length, 'items');
        console.log('First resume data:', JSON.stringify(response.data[0], null, 2));
        setResumes(response.data);
        setError(null);
      } else {
        console.error('Invalid response format:', response.data);
        setError('Received invalid data format from server');
        setResumes([]);
      }
    } catch (err) {
      console.error('Failed to load resumes:', err);
      setError(err.response?.data?.error || 'Failed to load resume history');
      setResumes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Extract unique skills from all resumes
    const skills = new Set();
    resumes.forEach(resume => {
      if (resume.data.skills) {
        resume.data.skills.forEach(skill => skills.add(skill.toLowerCase()));
      }
    });
    setAvailableSkills(skills);

    // Apply filters
    let filtered = [...resumes];

    // Text search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(resume => 
        resume.filename.toLowerCase().includes(searchLower) ||
        resume.data.name?.toLowerCase().includes(searchLower) ||
        resume.data.skills?.some(skill => skill.toLowerCase().includes(searchLower))
      );
    }

    // Skills filter
    if (selectedSkills.length > 0) {
      filtered = filtered.filter(resume =>
        selectedSkills.every(skill =>
          resume.data.skills?.some(s => s.toLowerCase() === skill.toLowerCase())
        )
      );
    }

    setFilteredResumes(filtered);
  }, [resumes, searchTerm, selectedSkills]);

  // Refresh resumes after successful upload
  const handleRefresh = () => {
    console.log('Manual refresh triggered');
    setLoading(true);
    loadResumes();
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedSkills([]);
  };

  if (loading) {
    return <div className="mt-4">Loading resumes...</div>;
  }

  if (error) {
    return (
      <div className="alert alert-danger mt-4">
        <h4>Error Loading Resumes</h4>
        <p>{error}</p>
        <button className="btn btn-primary mt-2" onClick={loadResumes}>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3>Previously Processed Resumes ({filteredResumes.length})</h3>
        <button 
          className="btn btn-outline-primary" 
          onClick={handleRefresh}
          disabled={loading}
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {/* Filters Section */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="card-title mb-0">Filters</h5>
            <button 
              className="btn btn-outline-secondary btn-sm"
              onClick={clearFilters}
              disabled={!searchTerm && selectedSkills.length === 0}
            >
              Clear Filters
            </button>
          </div>
          <div className="row g-3">
            {/* Search Input */}
            <div className="col-md-12">
              <input
                type="text"
                className="form-control"
                placeholder="Search by name, skills, or filename..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            {/* Skills Filter */}
            <div className="col-md-12">
              <select
                className="form-select"
                multiple
                value={selectedSkills}
                onChange={(e) => {
                  const values = Array.from(e.target.selectedOptions, option => option.value);
                  setSelectedSkills(values);
                }}
              >
                {Array.from(availableSkills).sort().map(skill => (
                  <option key={skill} value={skill}>
                    {skill}
                  </option>
                ))}
              </select>
              <small className="text-muted">Hold Ctrl/Cmd to select multiple skills</small>
            </div>
          </div>
        </div>
      </div>

      {(!filteredResumes || filteredResumes.length === 0) ? (
        <div className="alert alert-info">
          {resumes.length === 0 ? 
            "No resumes processed yet. Upload your first resume above!" :
            "No resumes match the current filters."
          }
        </div>
      ) : (
        <div className="resume-list">
          {filteredResumes.map((resume) => (
            <div key={resume.id} className="card mb-3">
              <div className="card-header">
                <h5 className="mb-0">
                  {resume.filename}
                  <small className="text-muted ms-2">
                    {new Date(resume.created_at).toLocaleString()}
                  </small>
                </h5>
              </div>
              <div className="card-body">
                <ResumeSummary data={resume.data} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ResumeHistory;
