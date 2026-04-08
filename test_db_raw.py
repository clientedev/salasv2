import os
import sqlalchemy

db_url = 'postgresql://postgres:TmwXrUExIhipfFtkuClUZWobYGOHHGMu@turntable.proxy.rlwy.net:58753/railway'
#Railway external connections often drop without sslmode or with strict sslmode, let's just try using raw psycopg2 without flask first to see if it responds!
import psycopg2
try:
    print("Connecting raw...")
    conn = psycopg2.connect(db_url)
    print("Raw connection successful!")
    
    # Try fetching a school
    cur = conn.cursor()
    cur.execute("SELECT * FROM school")
    print(cur.fetchall())
except Exception as e:
    import traceback
    traceback.print_exc()
