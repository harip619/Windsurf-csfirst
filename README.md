# Resume Parser Application

A full-stack application for parsing and managing resumes, built inside the Windsurf development environment.

## Project Description

This application allows users to:
- Upload resume files (PDF, DOCX)
- Extract key information automatically
- View parsed resume data in a structured format
- Filter resumes by search terms and skills
- Manage resume history with real-time filtering

## How to Run

The application is containerized using Docker for easy deployment:

```bash
# Start both frontend and backend services
docker-compose up
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Routes

### Frontend Routes
- `/` - Home page
- `/upload` - Upload new resumes
- `/history` - View and filter parsed resumes

### API Routes
- `POST /api/upload` - Upload and parse a new resume
- `GET /api/resumes` - Get all parsed resumes

## Technologies Used

### Frontend
- React with Vite
- React Router for navigation
- Axios for API requests
- Bootstrap for styling

### Backend
- Flask (Python)
- SQLite for data storage
- Resume parsing libraries

### Infrastructure
- Docker and Docker Compose
- Nginx for API proxy

## Development Environment

This project was developed using the Windsurf development environment, which provides:
- Containerized development
- Hot reload for both frontend and backend
- Integrated database management
- API proxy configuration
