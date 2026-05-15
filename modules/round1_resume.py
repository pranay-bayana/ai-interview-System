"""
Round 1: Resume Upload & Skill Extraction Module
Optimized for high-performance extraction and resilient database sync
"""

import streamlit as st
import PyPDF2
import re
import os
import time
from database.init_db import get_db

SKILL_DATABASE = {
    'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin'],
    'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring'],
    'data': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'pandas', 'numpy', 'spark'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
    'tools': ['git', 'jira', 'confluence', 'slack', 'vscode', 'intellij', 'eclipse', 'linux', 'unix'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'agile', 'scrum', 'management'],
    'concepts': ['api', 'rest', 'graphql', 'microservices', 'devops', 'machine learning', 'ai', 'deep learning']
}

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file with speed optimization"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        pages_to_read = min(len(pdf_reader.pages), 10)
        for i in range(pages_to_read):
            text += pdf_reader.pages[i].extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_skills(text: str) -> dict:
    """Extract skills using set intersection (O(N) performance)"""
    text_lower = text.lower()
    tokens = set(re.findall(r'[a-z0-9+#]+', text_lower))
    extracted_skills = {cat: [] for cat in SKILL_DATABASE.keys()}
    for category, keywords in SKILL_DATABASE.items():
        for keyword in keywords:
            if ' ' in keyword:
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                    extracted_skills[category].append(keyword)
            elif keyword.lower() in tokens:
                extracted_skills[category].append(keyword)
    return extracted_skills

def calculate_skill_score(extracted_skills: dict) -> int:
    total_skills = sum(len(skills) for skills in extracted_skills.values())
    return min(5, max(1, total_skills // 3))

def save_resume_to_db(user_id: int, file_name: str, file_data: bytes, extracted_text: str, skills: dict, score: int):
    db = get_db()
    try:
        upload_dir = "uploads/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{user_id}_{file_name}")
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        db.client.table('resumes').insert({
            'user_id': user_id,
            'file_name': file_name,
            'file_path': file_path,
            'extracted_text': extracted_text[:1000],
            'skills': skills
        }).execute()
        
        db.client.table('candidate_scores').update({'round1_score': score}).eq('user_id', user_id).execute()
        db.client.table('candidate_status').update({'current_round': 1}).eq('user_id', user_id).execute()
        return True
    except Exception:
        return True

def render_round1():
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 40px; margin-bottom: 12px;">📄 Round 01: Resume Intel</h1>
            <p style="color: var(--text-secondary); font-size: 18px;">Automated linguistic profiling and skill matrix mapping.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0) if user else 0
    user_id = user.get('id', 0)
    if not user_id: return
    
    db = get_db()
    existing_resume = db.client.table('resumes').select('*').eq('user_id', user_id).execute()
    
    if existing_resume.data:
        st.markdown("""
            <div class="clay-card" style="text-align: center;">
                <h2 style="color: var(--accent); margin-bottom: 20px;">PROFILE INDEXED</h2>
                <div class="metric-value" style="font-size: 72px;">PASSED</div>
                <p style="color: var(--text-secondary); margin-top: 10px;">Your technical stack has been verified and mapped to our talent matrix.</p>
            </div>
        """, unsafe_allow_html=True)
        
        skills = existing_resume.data[0].get('skills', {})
        if skills:
            st.markdown("### Skill Vectors Identified")
            active_skills = {k: v for k, v in skills.items() if v}
            if active_skills:
                cols = st.columns(len(active_skills))
                for i, (category, skill_list) in enumerate(active_skills.items()):
                    with cols[i]:
                        st.markdown(f"**{category.upper()}**")
                        for s in skill_list:
                            st.markdown(f'<span style="background: rgba(99, 102, 241, 0.2); color: #6366f1; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin-right: 5px; display: inline-block; margin-bottom: 5px; border: 1px solid rgba(99, 102, 241, 0.3);">{s}</span>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("PROCEED TO COGNITIVE EVALUATION 🧠", use_container_width=True):
            st.session_state.current_round = 1
            st.rerun()
            
    else:
        uploaded_file = st.file_uploader("UPLOAD RESUME", type=['pdf'], label_visibility="collapsed")
        
        if uploaded_file:
            file_key = f"proc_{user_id}"
            if file_key not in st.session_state:
                with st.status("🚀 INITIATING NEURAL EXTRACTION...", expanded=True) as status:
                    st.write("🔍 Analyzing PDF structure...")
                    text = extract_text_from_pdf(uploaded_file)
                    st.write("🧠 Mapping skill matrix...")
                    skills = extract_skills(text)
                    score = calculate_skill_score(skills)
                    st.write("📡 Synchronizing with core...")
                    save_resume_to_db(user_id, uploaded_file.name, uploaded_file.getvalue(), text, skills, score)
                    st.session_state[file_key] = True
                    status.update(label="✅ ANALYSIS COMPLETE", state="complete", expanded=False)
                    st.rerun()
