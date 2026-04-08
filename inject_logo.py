
from app import app, db
from models import School
import os

with app.app_context():
    school = School.query.get(1)
    if school:
        # Create a small red pixel PNG as test data
        test_logo = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\x0dcG\x04\x00\x00\x00\x00IEND\xaeB`\x82'
        school.logo_data = test_logo
        school.logo_mimetype = 'image/png'
        db.session.commit()
        print(f"Successfully added test logo to school: {school.name}")
    else:
        print("School with ID 1 not found")
