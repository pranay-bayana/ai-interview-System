"""
Admin Decision Desk Module
World-Class Talent Management Terminal
"""

import streamlit as st
import pandas as pd
from database.init_db import get_db

def get_all_candidates() -> list:
    """Get all candidates with comprehensive intelligence metrics"""
    db = get_db()
    try:
        users_result = db.client.table('users').select('*').eq('role', 'candidate').execute()
        users = users_result.data or []
        
        candidates = []
        for user in users:
            uid = user.get('id', 0)
            
            # Fetch scores
            s_res = db.client.table('candidate_scores').select('*').eq('user_id', uid).execute()
            s = s_res.data[0] if s_res.data else {}
            
            # Fetch status
            st_res = db.client.table('candidate_status').select('*').eq('user_id', uid).execute()
            status = st_res.data[0] if st_res.data else {}
            
            # Fetch resume
            r_res = db.client.table('resumes').select('*').eq('user_id', uid).execute()
            resume = r_res.data[0] if r_res.data else {}
            
            # Calculate total (out of 60)
            total = sum([s.get(f'round{i}_score', 0) for i in range(1, 7)])
            
            candidates.append({
                'id': uid,
                'name': user.get('full_name', 'UNKNOWN_ENTITY'),
                'email': user.get('email', ''),
                'total_score': total,
                'r1': s.get('round1_score', 0),
                'r2': s.get('round2_score', 0),
                'r3': s.get('round3_score', 0),
                'r4': s.get('round4_score', 0),
                'r5': s.get('round5_score', 0),
                'r6': s.get('round6_score', 0),
                'status': status.get('status', 'pending'),
                'round': status.get('current_round', 0),
                'resume': resume.get('file_name', 'N/A')
            })
        return candidates
    except Exception as e:
        st.error(f"NEURAL_DB_SYNC_ERROR: {str(e)}")
        return []

def render_admin_dashboard():
    """Render Hyper-Futuristic Admin Terminal"""
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 48px; margin-bottom: 12px; font-weight: 900;">🎯 CONTROL CENTER</h1>
            <p style="color: var(--text-secondary); font-size: 20px;">Global oversight of neural talent acquisition and candidate clearance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    candidates = get_all_candidates()
    if not candidates:
        st.info("NO ACTIVE CANDIDATE SIGNATURES DETECTED IN THE NEURAL CORE.")
        return
    
    df = pd.DataFrame(candidates)
    
    # Premium Neural Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="clay-card" style="text-align: center; padding: 20px;"><div style="font-size: 10px; letter-spacing: 2px;">TOTAL ENTITIES</div><div class="metric-value" style="font-size: 48px;">{len(df)}</div></div>', unsafe_allow_html=True)
    with col2:
        cleared = len(df[df["status"]=="selected"])
        st.markdown(f'<div class="clay-card" style="text-align: center; padding: 20px;"><div style="font-size: 10px; letter-spacing: 2px; color: var(--accent);">CLEARED</div><div class="metric-value" style="font-size: 48px; color: var(--accent);">{cleared}</div></div>', unsafe_allow_html=True)
    with col3:
        pending = len(df[df["status"]=="pending"])
        st.markdown(f'<div class="clay-card" style="text-align: center; padding: 20px;"><div style="font-size: 10px; letter-spacing: 2px;">EVALUATING</div><div class="metric-value" style="font-size: 48px;">{pending}</div></div>', unsafe_allow_html=True)
    with col4:
        flagged = len(df[df["status"]=="rejected"])
        st.markdown(f'<div class="clay-card" style="text-align: center; padding: 20px;"><div style="font-size: 10px; letter-spacing: 2px; color: #ff6b6b;">FLAGGED</div><div class="metric-value" style="font-size: 48px; color: #ff6b6b;">{flagged}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    
    # Interactive Candidate Terminal
    for _, candidate in df.iterrows():
        status_color = "var(--accent)" if candidate['status'] == "selected" else "#ff6b6b" if candidate['status'] == "rejected" else "white"
        
        with st.expander(f"ENTITY: {candidate['name'].upper()} | AGGREGATE SCORE: {candidate['total_score']}/60 | STATUS: {candidate['status'].upper()}", expanded=False):
            st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1.5, 1, 1])
            with c1:
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border-left: 4px solid var(--primary);">
                        <p style="margin: 0; font-size: 14px; font-weight: 800; color: var(--primary);">PRIMARY INTEL</p>
                        <p style="margin: 10px 0 0 0;"><b>Email:</b> {candidate['email']}</p>
                        <p style="margin: 5px 0 0 0;"><b>Resume:</b> {candidate['resume']}</p>
                        <p style="margin: 5px 0 0 0;"><b>Neural Progress:</b> Round {candidate['round']}/7</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.write("**Assessment Breakdown**")
                st.write(f"🧠 Aptitude: {candidate['r2']}/10")
                st.write(f"💻 Technical: {candidate['r3']}/10")
                st.write(f"⌨️ Coding: {candidate['r4']}/10")
            
            with c3:
                st.write("**Neural Breakdown**")
                st.write(f"📄 Resume: {candidate['r1']}/10")
                st.write(f"🎙️ Voice: {candidate['r5']}/10")
                st.write(f"🤖 AI Chat: {candidate['r6']}/10")

            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
            ctrl1, ctrl2, ctrl3 = st.columns(3)
            db = get_db()
            
            with ctrl1:
                if st.button("APPROVE CLEARANCE 🟢", key=f"sel_{candidate['id']}", use_container_width=True):
                    db.client.table('candidate_status').update({'status': 'selected'}).eq('user_id', candidate['id']).execute()
                    st.success(f"Clearance Granted: {candidate['name']}")
                    st.rerun()
            with ctrl2:
                if st.button("FLAG FOR REJECTION 🔴", key=f"rej_{candidate['id']}", use_container_width=True):
                    db.client.table('candidate_status').update({'status': 'rejected'}).eq('user_id', candidate['id']).execute()
                    st.warning(f"Entity Flagged: {candidate['name']}")
                    st.rerun()
            with ctrl3:
                if st.button("NEURAL REFRESH 🔄", key=f"ref_{candidate['id']}", use_container_width=True):
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
