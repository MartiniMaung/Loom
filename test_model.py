import json
from src.loom.core import OSSProject

print("Testing OSSProject model with security_score...")

# Test data matching our JSON structure
test_data = {
    "name": "TestProject",
    "description": "Test description",
    "github_url": None,
    "capabilities": ["web_framework"],
    "license": "MIT",
    "popularity_score": 0.9,
    "security_score": 0.75,  # This should work now
    "compatibility_tags": ["test"],
    "metadata": {}
}

try:
    project = OSSProject(**test_data)
    print(f"✅ Successfully created OSSProject with security_score: {project.security_score}")
except Exception as e:
    print(f"❌ Error creating OSSProject: {e}")
    print(f"Error type: {type(e)}")
