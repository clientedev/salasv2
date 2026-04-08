import io
from app import app, db
from models import School

def inject_logo_2():
    with app.app_context():
        school = School.query.get(2)
        if school:
            # Simple blue square as logo for testing school 2
            from PIL import Image
            img = Image.new('RGB', (100, 100), color = (0, 0, 255))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            school.logo_data = img_byte_arr.getvalue()
            school.logo_mimetype = 'image/png'
            db.session.commit()
            print(f"Logo injected for {school.name}")
        else:
            print("School 2 not found")

if __name__ == "__main__":
    inject_logo_2()
