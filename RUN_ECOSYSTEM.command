#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting AI Recruitment Ecosystem..."
echo "📦 Installing/Verifying Dependencies..."
python3 -m pip install -r requirements.txt
echo "🌐 Launching Streamlit Application..."
python3 -m streamlit run app.py
