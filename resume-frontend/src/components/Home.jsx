import React from 'react';
import { Link } from 'react-router-dom';
import { FaUpload, FaHistory, FaRobot, FaCheckCircle } from 'react-icons/fa';

function Home() {
  return (
    <div className="container mt-5">
      <div className="text-center mb-5">
        <h1 className="display-4 mb-3">Smart Resume Parser</h1>
        <p className="lead text-muted">
          Extract valuable information from your resume using AI-powered analysis
        </p>
      </div>

      <div className="row g-4 py-5">
        {/* Feature Cards */}
        <div className="col-md-4">
          <div className="card h-100 shadow-sm hover-card">
            <div className="card-body text-center">
              <div className="feature-icon bg-primary bg-gradient text-white rounded-circle mb-3">
                <FaUpload className="bi" size={24} />
              </div>
              <h3 className="card-title h5">Easy Upload</h3>
              <p className="card-text">
                Simply upload your PDF resume and get instant results
              </p>
              <Link to="/upload" className="btn btn-primary">
                Upload Resume
              </Link>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card h-100 shadow-sm hover-card">
            <div className="card-body text-center">
              <div className="feature-icon bg-success bg-gradient text-white rounded-circle mb-3">
                <FaRobot className="bi" size={24} />
              </div>
              <h3 className="card-title h5">AI-Powered Analysis</h3>
              <p className="card-text">
                Advanced algorithms extract key information automatically
              </p>
              <ul className="list-unstyled text-start">
                <li><FaCheckCircle className="text-success me-2" /> Contact Information</li>
                <li><FaCheckCircle className="text-success me-2" /> Technical Skills</li>
                <li><FaCheckCircle className="text-success me-2" /> Work Experience</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card h-100 shadow-sm hover-card">
            <div className="card-body text-center">
              <div className="feature-icon bg-info bg-gradient text-white rounded-circle mb-3">
                <FaHistory className="bi" size={24} />
              </div>
              <h3 className="card-title h5">Resume History</h3>
              <p className="card-text">
                Access your previously processed resumes anytime
              </p>
              <Link to="/history" className="btn btn-info text-white">
                View History
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center mt-5">
        <Link to="/upload" className="btn btn-primary btn-lg px-4 me-md-2">
          Get Started
        </Link>
        <Link to="/history" className="btn btn-outline-secondary btn-lg px-4">
          View History
        </Link>
      </div>
    </div>
  );
}

export default Home;
