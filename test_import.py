import sys
import traceback
print("Starting isolated test...")
try:
    import app
except Exception as e:
    traceback.print_exc()

print("App imported. Let's look at sys.modules['models']")
try:
    models = sys.modules['models']
    print(dir(models))
    print(models.__file__)
except KeyError:
    print("models not in sys.modules")

try:
    from models import School
    print("School imported successfully!")
except Exception as e:
    traceback.print_exc()
