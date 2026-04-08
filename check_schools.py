import sqlite3
import os

db_path = 'instance/senai_classrooms.db'
if not os.path.exists(db_path):
    print(f"Database {db_path} not found!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, logo_data IS NOT NULL, logo_mimetype FROM school")
    schools = cursor.fetchall()
    print("Schools in DB:")
    for s in schools:
        print(f"ID: {s[0]}, Name: {s[1]}, Has Logo: {s[2]}, Mime: {s[3]}")
    conn.close()
