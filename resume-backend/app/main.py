import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from extractor import extract_resume_data

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database setup
UPLOAD_FOLDER = 'app/uploads'
DB_PATH = 'app/resume_data.db'

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    logger.info("Initializing database...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  data TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    
    # Check if table exists and has records
    c.execute('SELECT COUNT(*) FROM resumes')
    count = c.fetchone()[0]
    logger.info(f"Database initialized. Found {count} existing records.")
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok", "message": "Server is running"})

@app.route('/resumes', methods=['GET'])
def get_resumes():
    logger.info("GET /resumes called")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get all resumes ordered by creation date
        c.execute('SELECT id, filename, data, created_at FROM resumes ORDER BY created_at DESC')
        rows = c.fetchall()
        
        # Format the results
        resumes = []
        for row in rows:
            try:
                # Debug log
                logger.debug(f"Processing row: {row}")
                
                # Ensure data is valid JSON
                if isinstance(row[2], str):
                    try:
                        data = json.loads(row[2])
                        logger.debug(f"Parsed JSON data: {data}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        logger.debug(f"Raw data: {row[2]}")
                        continue
                else:
                    data = row[2]
                
                resume = {
                    'id': row[0],
                    'filename': row[1],
                    'data': data,
                    'created_at': row[3]
                }
                resumes.append(resume)
                logger.debug(f"Added resume: {resume}")
            except Exception as e:
                logger.error(f"Error processing resume {row[0]}: {str(e)}")
                continue
        
        logger.info(f"Returning {len(resumes)} resumes")
        logger.debug(f"Full response: {resumes}")
        return jsonify(resumes)
        
    except Exception as e:
        logger.error(f"Error in get_resumes: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/upload', methods=['POST'])
def upload_resume():
    logger.info("POST /upload called")
    if 'resume' not in request.files:
        logger.error("No file in request")
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['resume']
    if file.filename == '':
        logger.error("Empty filename")
        return jsonify({'error': 'No file selected'}), 400
        
    try:
        # Save file and process
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)
        
        # Extract data from the resume
        logger.info("Extracting data from resume...")
        data = extract_resume_data(filepath)
        logger.debug(f"Extracted data: {data}")
        
        # Validate data structure
        if not isinstance(data, dict):
            logger.error(f"Invalid data structure: {data}")
            return jsonify({'error': 'Invalid data structure'}), 500
            
        required_fields = ['name', 'email', 'phone', 'skills', 'work_experience']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                data[field] = "" if field not in ['skills', 'work_experience'] else []
        
        # Store in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Convert data to JSON string
        json_data = json.dumps(data)
        logger.debug(f"Storing JSON data: {json_data}")
        
        c.execute('INSERT INTO resumes (filename, data) VALUES (?, ?)',
                 (filename, json_data))
        conn.commit()
        
        # Get the inserted record
        c.execute('SELECT id, filename, data, created_at FROM resumes WHERE id = last_insert_rowid()')
        row = c.fetchone()
        
        result = {
            'id': row[0],
            'filename': row[1],
            'data': json.loads(row[2]),
            'created_at': row[3]
        }
        
        logger.info(f"Successfully processed and stored resume: {result['id']}")
        logger.debug(f"Return data: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in upload_resume: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)  # Clean up the uploaded file
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
