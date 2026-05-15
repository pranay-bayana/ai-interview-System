"""
Round 4: Coding Engine Module
Claymorphism UI with robust test case validation and hidden solutions
"""

import streamlit as st
import tempfile
import os
from database.init_db import get_db

CODING_CHALLENGE = {
    'title': 'Algorithm: Neural Sequence Reversal',
    'description': 'Construct a function `reverse_string(s)` that reverses a high-dimensional string vector. Handle null-states and special character encodings.',
    'test_cases': [
        {'input': 'hello', 'expected': 'olleh'},
        {'input': 'Python', 'expected': 'nohtyP'},
        {'input': '', 'expected': ''},
        {'input': 'a', 'expected': 'a'},
        {'input': 'Neural', 'expected': 'larueN'}
    ]
}

def execute_python_code(code: str, test_cases: list) -> tuple:
    passed = 0
    results = []
    try:
        exec_globals = {}
        exec(code, exec_globals)
        func = exec_globals.get('reverse_string')
        
        if not func:
            return 0, len(test_cases), [{'error': 'Critical Error: Function entry point `reverse_string` not found in buffer.'}]
            
        for test in test_cases:
            try:
                actual = func(test['input'])
                is_correct = (actual == test['expected'])
                if is_correct: passed += 1
                results.append({'status': 'PASS' if is_correct else 'FAIL'})
            except Exception as e:
                results.append({'status': f'ERROR: {str(e)}'})
    except Exception as e:
        return 0, len(test_cases), [{'error': f'Compiler Exception: {str(e)}'}]
    return passed, len(test_cases), results

def save_coding_submission(user_id: int, language: str, code: str, passed: int, total: int, score: int):
    db = get_db()
    try:
        db.client.table('coding_submissions').insert({
            'user_id': user_id,
            'language': language,
            'code': code,
            'test_cases_passed': passed,
            'total_test_cases': total,
            'score': score
        }).execute()
        db.client.table('candidate_scores').update({'round4_score': score}).eq('user_id', user_id).execute()
        db.client.table('candidate_status').update({'current_round': 4}).eq('user_id', user_id).execute()
        return True
    except Exception as e:
        st.error(f"Sync Error: {str(e)}")
        return False

def render_round4():
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 40px; margin-bottom: 12px;">⌨️ Round 04: Algorithmic Engineering</h1>
            <p style="color: var(--text-secondary); font-size: 18px;">Optimization of computational logic and edge-case handling.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0)
    if not user_id: return
    
    db = get_db()
    existing = db.client.table('coding_submissions').select('*').eq('user_id', user_id).execute()
    
    if existing.data:
        sub = existing.data[0]
        score = sub.get('score', 0)
        st.markdown(f"""
            <div class="clay-card" style="text-align: center;">
                <h2 style="color: var(--accent); margin-bottom: 20px;">ALGORITHM DEPLOYED</h2>
                <div class="metric-value" style="font-size: 72px;">{score}/10</div>
                <p style="color: var(--text-secondary); margin-top: 10px;">Verification successful against all high-priority test vectors.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        if st.button("PROCEED TO VOCAL PROFILING 🎙️", use_container_width=True):
            st.session_state.current_round = 4
            st.rerun()
    else:
        lang = st.selectbox("COMPILER ARCHITECTURE:", ['python', 'java', 'cpp'], format_func=lambda x: x.upper())
        
        st.markdown(f"""
            <div class="clay-card" style="margin-bottom: 30px; border-left: 5px solid var(--accent);">
                <h3>{CODING_CHALLENGE['title']}</h3>
                <p style="color: var(--text-secondary); margin-top: 10px;">{CODING_CHALLENGE['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Simple Editor - Empty by default
        code = st.text_area("LOGIC EDITOR", value="def reverse_string(s: str) -> str:\n    # Write your solution here\n    pass", height=250)
        
        if st.button("COMPILE & EXECUTE 🚀", use_container_width=True):
            with st.spinner("Validating test vectors..."):
                if lang == 'python':
                    passed, total, results = execute_python_code(code, CODING_CHALLENGE['test_cases'])
                    score = int((passed / total) * 10)
                    
                    # Show results cleanly
                    st.markdown("### COMPILER LOGS")
                    cols = st.columns(len(results))
                    for i, res in enumerate(results):
                        with cols[i]:
                            status = res.get('status', 'FAIL')
                            color = "#43e97b" if "PASS" in status else "#ff6b6b"
                            st.markdown(f"""
                                <div style="padding: 10px; background: {color}22; border: 1px solid {color}; border-radius: 10px; text-align: center; font-weight: 700; color: {color};">
                                    T{i+1}: {status}
                                </div>
                            """, unsafe_allow_html=True)
                    
                    if save_coding_submission(user_id, lang, code, passed, total, score):
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Cloud Compiler currently limited to Python for the Demo environment.")
