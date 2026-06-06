"""
PythonAnywhere WSGI configuration file
Upload to PythonAnywhere and set as WSGI configuration
"""
import sys
import os

# Set the project path on PythonAnywhere
# Replace 'yourusername' with your PythonAnywhere username
project_home = '/home/yourusername/tongue-diagnosis'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import app as application
