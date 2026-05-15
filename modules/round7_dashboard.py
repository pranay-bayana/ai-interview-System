"""
Round 7: Performance Dashboard Module
World-Class Dashboard with Real-Time Neural Mapping
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database.init_db import get_db

def ensure_score_row(user_id: int):
    """Ensure a row exists in candidate_scores for the user"""
    db = get_db()
    res = db.client.table('candidate_scores').select('*').eq('user_id', user_id).execute()
    if not res.data:
        db.client.table('candidate_scores').insert({'user_id': user_id}).execute()
    
    res_status = db.client.table('candidate_status').select('*').eq('user_id', user_id).execute()
    if not res_status.data:
        db.client.table('candidate_status').insert({'user_id': user_id, 'status': 'pending', 'current_round': 0}).execute()

def get_candidate_performance(user_id: int) -> dict:
    db = get_db()
    ensure_score_row(user_id)
    try:
        scores_res = db.client.table('candidate_scores').select('*').eq('user_id', user_id).execute()
        scores = scores_res.data[0] if scores_res.data else {}
        
        status_res = db.client.table('candidate_status').select('*').eq('user_id', user_id).execute()
        status = status_res.data[0] if status_res.data else {}
        
        return {'scores': scores, 'status': status}
    except Exception:
        return {}

def render_round7():
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 44px; margin-bottom: 12px; font-weight: 900;">📊 Performance Intelligence</h1>
            <p style="color: var(--text-secondary); font-size: 20px;">Neural analysis of your 7-stage interview journey.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0)
    if not user_id: return
    
    perf = get_candidate_performance(user_id)
    scores = perf.get('scores', {})
    
    if not scores:
        st.error("DATABASE_SYNC_ERROR: No intelligence vectors found.")
        return
    
    # Accurate Total Score Calculation (Out of 60)
    rounds = {
        "Resume": scores.get('round1_score', 0),
        "Aptitude": scores.get('round2_score', 0),
        "Technical": scores.get('round3_score', 0),
        "Coding": scores.get('round4_score', 0),
        "Voice": scores.get('round5_score', 0),
        "Chatbot": scores.get('round6_score', 0)
    }
    
    total = sum(rounds.values())
    max_possible = 60
    percentage = (total / max_possible) * 100
    
    st.markdown(f"""
        <div class="clay-card" style="text-align: center; border-top: 8px solid var(--accent);">
            <div style="font-size: 64px; margin-bottom: 10px;">{'🏆' if total > 40 else '✨'}</div>
            <h2 style="font-size: 32px; margin-bottom: 5px;">AGGREGATE NEURAL SCORE</h2>
            <div class="metric-value" style="font-size: 84px;">{total}/{max_possible}</div>
            <p style="color: var(--text-secondary); font-size: 18px;">Overall Performance Integrity: {percentage:.1f}%</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="clay-card">', unsafe_allow_html=True)
        st.markdown("### Vector Mapping")
        df = pd.DataFrame(list(rounds.items()), columns=['Phase', 'Score'])
        fig = px.line_polar(df, r='Score', theta='Phase', line_close=True)
        fig.update_traces(fill='toself', line_color='#6366f1', fillcolor='rgba(99, 102, 241, 0.4)')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          font_color='white', polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="clay-card">', unsafe_allow_html=True)
        st.markdown("### Phase Intelligence")
        for phase, score in rounds.items():
            color = "#43e97b" if score >= 8 else "#6366f1" if score >= 5 else "#ff6b6b"
            st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: 700;">{phase}</span>
                        <span style="color: {color}; font-weight: 800;">{score}/10</span>
                    </div>
                    <div style="height: 10px; background: rgba(255,255,255,0.05); border-radius: 5px; overflow: hidden;">
                        <div style="width: {score*10}%; height: 100%; background: {color};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if total >= 40:
        st.success("🎉 CONGRATULATIONS: You have been identified as an ELITE CANDIDATE. Our team will contact you shortly.")
    else:
        st.info("Assessment Complete. Your performance data has been indexed for future opportunities.")
