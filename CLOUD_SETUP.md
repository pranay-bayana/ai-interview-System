# 🚀 AI Recruitment Ecosystem: Cloud Setup Guide

To ensure the high-performance features (Voice Transcription, Database Persistence, AI Chatbot) work correctly, please follow these steps to set up your cloud infrastructure.

## 1. Supabase (Database)
We use Supabase for persistent storage of candidates, scores, and security violations.

1.  Go to [Supabase](https://supabase.com/) and create a new project.
2.  In your project dashboard, go to **Project Settings > API**.
3.  Copy the **Project URL** and **anon public Key**.
4.  Run the SQL provided in `database/schema.sql` in the **SQL Editor** of your Supabase dashboard to initialize the tables.

## 2. OpenAI (AI Intelligence)
Required for Whisper STT (Round 5) and the GPT-powered Technical Round (Round 3).

1.  Go to [OpenAI Platform](https://platform.openai.com/).
2.  Create an **API Key**.

## 3. Environment Configuration
Create a `.env` file in the root directory and paste your keys:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
ADMIN_ACCESS_KEY=ADMIN2024
```

## 4. Dependencies
Install all required libraries including the new security and UI modules:

```bash
pip install -r requirements.txt
```

## 5. Launch the Application
Start the ecosystem with the following command:

```bash
streamlit run app.py
```

---
**Note:** For Face Detection (Round 1-5), ensure you grant camera permissions in your browser.
