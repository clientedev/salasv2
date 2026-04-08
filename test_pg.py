import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:TmwXrUExIhipfFtkuClUZWobYGOHHGMu@turntable.proxy.rlwy.net:58753/railway'

try:
    from app import app, db
    with app.app_context():
        # Try to execute a simple query to ensure the DB connects
        db.engine.connect()
        print("PG Connection Successful!")
except Exception as e:
    import traceback
    traceback.print_exc()
