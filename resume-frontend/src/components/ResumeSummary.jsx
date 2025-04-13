import React from 'react';

function ResumeSummary({ data }) {
  // Handle case where data is undefined or null
  if (!data) {
    return (
      <div className="alert alert-warning">
        No resume data available
      </div>
    );
  }

  // Ensure arrays exist
  const skills = Array.isArray(data.skills) ? data.skills : [];
  const workExperience = Array.isArray(data.work_experience) ? data.work_experience : [];

  return (
    <div className="card border-success p-4">
      <h4 className="text-success">Extracted Resume Information</h4>
      <hr />

      <p><strong>Name:</strong> {data.name || 'N/A'}</p>
      <p><strong>Email:</strong> {data.email || 'N/A'}</p>
      <p><strong>Phone:</strong> {data.phone || 'N/A'}</p>
      <p><strong>Skills:</strong> {skills.length ? skills.join(', ') : 'N/A'}</p>
      <p><strong>Work Experience:</strong></p>
      <ul className="list-group list-group-flush">
        {workExperience.length
          ? workExperience.map((exp, idx) => (
              <li key={idx} className="list-group-item">{exp}</li>
            ))
          : <li className="list-group-item">N/A</li>}
      </ul>
    </div>
  );
}

export default ResumeSummary;
