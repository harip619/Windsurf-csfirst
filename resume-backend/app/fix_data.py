import sqlite3
import json
import ast

def fix_resume_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('app/resume_data.db')
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute('SELECT id, data FROM resumes')
        rows = cursor.fetchall()
        
        print("\nFixing resume data...")
        for row in rows:
            try:
                # Try to parse the existing data
                if isinstance(row[1], str):
                    try:
                        # First try to parse as JSON
                        data = json.loads(row[1])
                    except json.JSONDecodeError:
                        # If that fails, try to parse as Python literal
                        data = ast.literal_eval(row[1])
                
                # Convert Python None to JSON null
                if data.get('phone') is None:
                    data['phone'] = ''
                
                # Ensure arrays are initialized
                if not isinstance(data.get('skills'), list):
                    data['skills'] = []
                if not isinstance(data.get('work_experience'), list):
                    data['work_experience'] = []
                
                # Convert to proper JSON string
                json_data = json.dumps(data)
                
                # Update the record
                cursor.execute('UPDATE resumes SET data = ? WHERE id = ?', (json_data, row[0]))
                print(f"Fixed record ID: {row[0]}")
                
            except Exception as e:
                print(f"Error fixing record {row[0]}: {e}")
                continue
        
        conn.commit()
        print("\nFinished fixing data!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_resume_data()
