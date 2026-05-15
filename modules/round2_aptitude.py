"""
Round 2: Aptitude Assessment Module
Timed MCQ assessment with one-by-one navigation and premium UI
"""

import streamlit as st
import time
from database.init_db import get_db

APTITUDE_QUESTIONS = [
    {
        'id': 1,
        'question': 'If a train travels at 60 km/h for 2 hours and then at 80 km/h for 3 hours, what is the average speed?',
        'options': ['68 km/h', '70 km/h', '72 km/h', '75 km/h'],
        'correct': 'c',
        'explanation': 'Total distance = (60×2) + (80×3) = 120 + 240 = 360 km. Total time = 5 hours. Average speed = 360/5 = 72 km/h.'
    },
    {
        'id': 2,
        'question': 'A number is increased by 20% and then decreased by 20%. What is the net change?',
        'options': ['0%', '4% decrease', '4% increase', 'No change'],
        'correct': 'b',
        'explanation': 'Let number = 100. After 20% increase = 120. After 20% decrease = 120 × 0.8 = 96. Net change = 4% decrease.'
    },
    {
        'id': 3,
        'question': 'If 5 workers can complete a task in 10 days, how many days will 10 workers take?',
        'options': ['2 days', '5 days', '10 days', '20 days'],
        'correct': 'b',
        'explanation': 'More workers, less time. 10 workers is double, so time is halved: 10/2 = 5 days.'
    },
    {
        'id': 4,
        'question': 'What is the next number in the sequence: 2, 6, 12, 20, 30, ?',
        'options': ['40', '42', '44', '46'],
        'correct': 'b',
        'explanation': 'Pattern: +4, +6, +8, +10, +12. So 30 + 12 = 42.'
    },
    {
        'id': 5,
        'question': 'A shopkeeper sells an item at 20% profit. If the cost price is $500, what is the selling price?',
        'options': ['$550', '$580', '$600', '$620'],
        'correct': 'c',
        'explanation': 'Profit = 20% of $500 = $100. Selling price = $500 + $100 = $600.'
    }
]

def calculate_aptitude_score(user_answers: dict) -> int:
    correct_count = 0
    for q in APTITUDE_QUESTIONS:
        if user_answers.get(q['id']) == q['correct']:
            correct_count += 1
    return correct_count

def save_aptitude_answers(user_id: int, user_answers: dict, score: int):
    db = get_db()
    try:
        for q_id, answer in user_answers.items():
            question = next((q for q in APTITUDE_QUESTIONS if q['id'] == q_id), None)
            if question:
                is_correct = (answer == question['correct'])
                db.client.table('aptitude_answers').insert({
                    'user_id': user_id,
                    'question_id': q_id,
                    'answer': answer,
                    'is_correct': is_correct
                }).execute()
        
        db.client.table('candidate_scores').update({'round2_score': score}).eq('user_id', user_id).execute()
        db.client.table('candidate_status').update({'current_round': 2}).eq('user_id', user_id).execute()
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def render_round2():
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 40px; margin-bottom: 12px;">🧠 Round 02: Cognitive Evaluation</h1>
            <p style="color: var(--text-dim); font-size: 18px;">One-by-one logical assessment with real-time navigation.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0) if user else 0
    user_id = user.get('id', 0)
    if not user_id: return
    
    db = get_db()
    existing = db.client.table('aptitude_answers').select('*').eq('user_id', user_id).execute()
    
    if existing.data:
        correct = sum(1 for ans in existing.data if ans.get('is_correct', False))
        st.markdown(f"""
            <div class="clay-card" style="text-align: center;">
                <h2 style="color: var(--accent); margin-bottom: 20px;">COGNITIVE PROFILE SYNCED</h2>
                <div class="metric-value" style="font-size: 72px;">{correct}/05</div>
                <p style="color: var(--text-secondary); margin-top: 10px;">Your analytical vectors have been validated and indexed.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        if st.button("PROCEED TO TECHNICAL 💻", use_container_width=True):
            st.session_state.current_round = 2
            st.rerun()
    else:
        if 'apt_q_idx' not in st.session_state: st.session_state.apt_q_idx = 0
        if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
        if 'apt_start_time' not in st.session_state: st.session_state.apt_start_time = time.time()
        
        # Timer
        elapsed = int(time.time() - st.session_state.apt_start_time)
        remaining = max(0, 600 - elapsed)
        st.markdown(f"""
            <div style="text-align: right; margin-bottom: 20px;">
                <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); font-weight: 700;">
                    ⏳ TIME REMAINING: {remaining//60:02d}:{remaining%60:02d}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        curr_q = APTITUDE_QUESTIONS[st.session_state.apt_q_idx]
        
        st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 30px; border-left: 5px solid #6366f1;">
                <div style="color: #6366f1; font-weight: 700; margin-bottom: 10px; font-size: 14px;">QUESTION {st.session_state.apt_q_idx + 1} OF 5</div>
                <h2 style="font-size: 24px; line-height: 1.5; color: #fff;">{curr_q['question']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        options = ['a', 'b', 'c', 'd']
        current_selection = st.session_state.user_answers.get(curr_q['id'])
        current_idx = options.index(current_selection) if current_selection in options else None
        
        selected = st.radio(
            "Select your answer:",
            options,
            index=current_idx,
            format_func=lambda x: f"{x.upper()}. {curr_q['options'][options.index(x)]}",
            key=f"apt_radio_{curr_q['id']}"
        )
        
        if selected:
            st.session_state.user_answers[curr_q['id']] = selected
        
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.apt_q_idx > 0:
                if st.button("⬅️ PREVIOUS", use_container_width=True):
                    st.session_state.apt_q_idx -= 1
                    st.rerun()
        with col3:
            if st.session_state.apt_q_idx < len(APTITUDE_QUESTIONS) - 1:
                if st.button("NEXT ➡️", use_container_width=True):
                    st.session_state.apt_q_idx += 1
                    st.rerun()
            else:
                if st.button("SUBMIT PROFILE 🎯", use_container_width=True, type="primary"):
                    score = calculate_aptitude_score(st.session_state.user_answers)
                    if save_aptitude_answers(user_id, st.session_state.user_answers, score):
                        st.balloons()
                        st.rerun()
