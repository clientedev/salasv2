import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:TmwXrUExIhipfFtkuClUZWobYGOHHGMu@turntable.proxy.rlwy.net:58753/railway'

from app import app
from flask.testing import FlaskClient

with app.test_client() as client:
    response = client.get('/', follow_redirects=True)
    print(f"Status: {response.status_code}")
    if response.status_code == 500:
        print("ERROR 500 CAUGHT!")
        print(response.get_data(as_text=True))
