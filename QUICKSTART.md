# Quick Start Guide - AI Recruitment Ecosystem

## Prerequisites

- Python 3.8 or higher
- Supabase account (free tier works)
- OpenAI API key (for Whisper STT - optional, system works without it)

## Setup Instructions

### 1. Install Dependencies

```bash
cd "AI intervuew system"
pip install -r requirements.txt
```

### 2. Set Up Supabase Database

1. Go to https://supabase.com and create a free account
2. Create a new project
3. Go to the SQL Editor in your Supabase dashboard
4. Copy and paste the contents of `database/schema.sql`
5. Click "Run" to execute the schema
6. Go to Project Settings > API
7. Copy your:
   - Project URL
   - anon/public key
   - service_role key (for admin operations)

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
OPENAI_API_KEY=your_openai_api_key  # Optional
ADMIN_ACCESS_KEY=ADMIN2024
```

### 4. Run Setup Script

```bash
python setup.py
```

This will create necessary directories and configuration files.

### 5. Install Playwright Browsers (for testing)

```bash
playwright install
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open at http://localhost:8501

## Usage

### For Candidates

1. Click "Login / Sign Up" in the sidebar
2. Create an account with your email and password
3. Navigate through the 7 interview rounds:
   - **Round 1**: Upload your resume (PDF)
   - **Round 2**: Complete aptitude MCQs (10 minutes)
   - **Round 3**: Answer technical questions (select your role)
   - **Round 4**: Solve the coding challenge (Python/Java/C++)
   - **Round 5**: Record voice responses to HR questions
   - **Round 6**: Chat with AI assistant for tips
   - **Round 7**: View your performance dashboard

### For Admins

1. Click "Admin Access" in the sidebar
2. Enter the access key (default: `ADMIN2024`)
3. View all candidates in the Decision Desk
4. Filter by status, score, or progress
5. Review candidate performance and download resumes
6. Update candidate status (Selected/Hold/Rejected)

## Running Tests

```bash
# Start the application in a terminal
streamlit run app.py

# In another terminal, run Playwright tests
pytest tests/test_e2e.py
```

## Project Structure

```
AI intervuew system/
├── app.py                    # Main application
├── setup.py                  # Setup script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── database/
│   ├── schema.sql           # Database schema
│   └── init_db.py           # Database connection
├── modules/
│   ├── auth.py              # Authentication
│   ├── round1_resume.py     # Resume upload
│   ├── round2_aptitude.py   # Aptitude test
│   ├── round3_technical.py  # Technical questions
│   ├── round4_coding.py     # Coding challenge
│   ├── round5_voice.py      # Voice interview
│   ├── round6_chatbot.py    # AI chatbot
│   ├── round7_dashboard.py  # Performance dashboard
│   └── admin.py             # Admin dashboard
├── static/
│   └── styles.css           # Glassmorphism CSS
├── tests/
│   ├── test_e2e.py          # Playwright tests
│   └── pytest.ini           # Pytest configuration
├── uploads/                 # Auto-created for file uploads
│   ├── resumes/
│   └── voice/
└── playwright.config.toml   # Playwright configuration
```

## Troubleshooting

### Database Connection Issues

- Verify your Supabase URL and keys in `.env`
- Ensure your Supabase project is active
- Check that the schema was executed successfully

### Audio Recording Issues

- Ensure microphone permissions are granted
- Check that sounddevice is installed correctly
- On macOS, you may need to grant microphone access to Python

### PDF Upload Issues

- Ensure the file is a valid PDF
- Check file size (max 10MB)
- Verify uploads directory exists

### OpenAI Whisper Issues

- The system works without OpenAI API key (uses simulated transcription)
- For real transcription, add your OpenAI API key to `.env`
- Ensure you have credits in your OpenAI account

## Features

- ✅ Premium Dark Glassmorphism UI
- ✅ 7-Stage Automated Interview Flow
- ✅ Cloud PostgreSQL Database (Supabase)
- ✅ Resume PDF Processing & Skill Extraction
- ✅ Timed Aptitude Assessment
- ✅ Role-based Technical Questions
- ✅ Multi-language Coding Engine
- ✅ Voice Interview with Whisper STT
- ✅ AI Chatbot Assistant
- ✅ Performance Dashboard with Charts
- ✅ Admin Decision Desk
- ✅ Playwright E2E Testing

## Support

For issues or questions, refer to the main README.md file.
