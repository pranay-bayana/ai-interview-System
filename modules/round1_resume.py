"""
Round 1: Resume Intelligence Module (Synchronized UI)
"""

import streamlit as st
import pdfplumber
import io
import re
from database.init_db import get_db

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def calculate_score(text):
    score = 0
    skills = []
    keywords = {
        'Python': 10, 'Java': 8, 'C++': 8, 'React': 10, 'Node.js': 10,
        'Machine Learning': 15, 'AI': 15, 'SQL': 7, 'Docker': 9, 'AWS': 12
    }
    for kw, val in keywords.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.I):
            score += val
            skills.append(kw)
    return min(score, 100), skills

def render_round1():
    # UI Header (Synced with Landing Page)
    st.markdown('<div class="section-label">ROUND 01</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text">RESUME INTEL</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Neural Document Analysis")
    st.write("Upload your technical profile for linguistic scoring and skill extraction.")
    
    uploaded_file = st.file_uploader("DROP PROFILE (PDF)", type="pdf", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        file_key = f"resume_processed_{uploaded_file.name}"
        if file_key not in st.session_state:
            with st.status("Initializing neural parser...", expanded=True) as status:
                st.write("Scanning vectors...")
                text = extract_text_from_pdf(uploaded_file.getvalue())
                st.write("Extracting linguistic patterns...")
                score, skills = calculate_score(text)
                
                normalized_score = min(score // 10, 10)
                # Display Results in Glass Card
                st.markdown('<div class="glass-card" style="border-left: 4px solid var(--indigo);">', unsafe_allow_html=True)
                st.markdown(f"#### 🏆 Profile Score: {normalized_score}/10")
                if skills:
                    st.write("**Detected Skillsets:**")
                    cols = st.columns(3)
                    for i, s in enumerate(skills):
                        cols[i % 3].markdown(f'<div class="feat-tag">{s}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                status.update(label="✅ ANALYSIS COMPLETE", state="complete", expanded=False)
                st.session_state[file_key] = True
                st.session_state[f"score_{file_key}"] = normalized_score

        if st.session_state.get(file_key):
            st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
            if st.button("PROCEED TO NEURAL APTITUDE →", use_container_width=True):
                user = st.session_state.get('user', {})
                user_id = user.get('id', 0)
                if user_id:
                    normalized_score = st.session_state.get(f"score_{file_key}", 0)
                    db = get_db()
                    db.client.table('candidate_scores').update({'round1_score': normalized_score}).eq('user_id', user_id).execute()
                    db.client.table('candidate_status').update({'current_round': 1}).eq('user_id', user_id).execute()
                st.session_state.current_round = 1
                st.rerun()
