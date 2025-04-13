import sqlite3
import json

def view_resume_table():
    try:
        # Connect to the database
        conn = sqlite3.connect('app/resume_data.db')
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute('SELECT id, filename, data, created_at FROM resumes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        if not rows:
            print("\nNo resumes found in the database.")
            return
            
        print("\nResume Table Contents:")
        print("=" * 80)
        for row in rows:
            print(f"\nID: {row[0]}")
            print(f"Filename: {row[1]}")
            print(f"Created At: {row[3]}")
            try:
                data = json.loads(row[2])
                print("Data:")
                for key, value in data.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                print(f"Error parsing data: {e}")
                print(f"Raw data: {row[2]}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_resume_table()
