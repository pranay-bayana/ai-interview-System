"""
Setup Script for AI Recruitment Ecosystem
Run this script to initialize the project
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'uploads/resumes',
        'uploads/voice',
        'static',
        'modules',
        'database',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Uploads
uploads/

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Logs
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_streamlit_config():
    """Create Streamlit configuration"""
    config_content = """[theme]
primaryColor = "#667eea"
backgroundColor = "#0a0a0f"
secondaryBackgroundColor = "#050508"
textColor = "#ffffff"
font = "sans serif"

[client]
showErrorDetails = false
maxUploadSize = 200

[logger]
level = "info"
"""
    
    Path('.streamlit').mkdir(exist_ok=True)
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    print("✓ Created Streamlit config")

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'psycopg2-binary',
        'sqlalchemy',
        'pandas',
        'numpy',
        'matplotlib',
        'PyPDF2',
        'sounddevice',
        'soundfile',
        'openai',
        'python-dotenv',
        'supabase',
        'playwright',
        'pytest-playwright',
        'Pillow',
        'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✓ All dependencies are installed")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI Recruitment Ecosystem...")
    print()
    
    # Create directories
    create_directories()
    print()
    
    # Create .gitignore
    create_gitignore()
    print()
    
    # Create Streamlit config
    create_streamlit_config()
    print()
    
    # Check dependencies
    check_dependencies()
    print()
    
    print("✅ Setup complete!")
    print()
    print("Next steps:")
    print("1. Copy .env.example to .env and configure your environment variables")
    print("2. Set up a Supabase project at https://supabase.com")
    print("3. Run the database schema from database/schema.sql in Supabase SQL Editor")
    print("4. Run: streamlit run app.py")
    print()

if __name__ == "__main__":
    main()
