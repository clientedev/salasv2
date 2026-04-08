
import os
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = "instance/senai_classrooms.db"
DEFAULT_SCHOOL_NAME = "SENAI Morvan Figueiredo"
DEFAULT_ADMIN_PASSWORD = "senai103103"

def migrate():
    if not os.path.exists(DB_PATH):
        logging.error(f"Database {DB_PATH} not found!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        logging.info("Creating school table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS school (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                admin_password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check if the default school already exists
        cursor.execute("SELECT id FROM school WHERE name = ?", (DEFAULT_SCHOOL_NAME,))
        result = cursor.fetchone()

        if not result:
            logging.info(f"Inserting default school: {DEFAULT_SCHOOL_NAME}")
            cursor.execute("INSERT INTO school (name, admin_password) VALUES (?, ?)", 
                           (DEFAULT_SCHOOL_NAME, DEFAULT_ADMIN_PASSWORD))
            school_id = cursor.lastrowid
        else:
            school_id = result[0]
            logging.info(f"Default school already exists with ID: {school_id}")

        # Add school_id column to classroom if it doesn't exist
        logging.info("Checking for school_id column in classroom table...")
        cursor.execute("PRAGMA table_info(classroom)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'school_id' not in columns:
            logging.info("Adding school_id column to classroom table...")
            cursor.execute("ALTER TABLE classroom ADD COLUMN school_id INTEGER REFERENCES school(id)")
        else:
            logging.info("school_id column already exists in classroom table.")

        # Update all classrooms to point to the default school
        logging.info(f"Linking all classrooms to school ID: {school_id}")
        cursor.execute("UPDATE classroom SET school_id = ? WHERE school_id IS NULL", (school_id,))

        conn.commit()
        logging.info("Migration completed successfully!")

    except Exception as e:
        logging.error(f"Migration failed: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate()
