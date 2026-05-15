"""
Round 3: Technical Questions Module
Role-based (Python/Java/QA) dynamic questions with keyword-based scoring
"""

import streamlit as st
from database.init_db import get_db

# Technical questions database by role
TECHNICAL_QUESTIONS = {
    'python': [
        {
            'id': 1,
            'question': 'Explain the difference between list and tuple in Python.',
            'keywords': ['mutable', 'immutable', 'brackets', 'parentheses', 'change', 'modify'],
            'max_score': 2
        },
        {
            'id': 2,
            'question': 'What is a decorator in Python? Give an example.',
            'keywords': ['function', 'wrapper', '@', 'modify', 'behavior', 'syntax'],
            'max_score': 2
        },
        {
            'id': 3,
            'question': 'Explain the GIL (Global Interpreter Lock) in Python.',
            'keywords': ['thread', 'execution', 'mutex', 'performance', 'concurrent', 'cpu'],
            'max_score': 2
        },
        {
            'id': 4,
            'question': 'What is the difference between __init__ and __new__?',
            'keywords': ['constructor', 'instance', 'object', 'creation', 'initialization', 'return'],
            'max_score': 2
        },
        {
            'id': 5,
            'question': 'Explain list comprehension and give an example.',
            'keywords': ['compact', 'syntax', 'iteration', 'expression', 'brackets', 'loop'],
            'max_score': 2
        }
    ],
    'java': [
        {
            'id': 1,
            'question': 'Explain the difference between == and .equals() in Java.',
            'keywords': ['reference', 'value', 'object', 'memory', 'address', 'comparison'],
            'max_score': 2
        },
        {
            'id': 2,
            'question': 'What is the difference between ArrayList and LinkedList?',
            'keywords': ['array', 'node', 'random', 'access', 'insertion', 'performance'],
            'max_score': 2
        },
        {
            'id': 3,
            'question': 'Explain the concept of polymorphism in Java.',
            'keywords': ['overriding', 'overloading', 'inheritance', 'method', 'behavior', 'multiple'],
            'max_score': 2
        },
        {
            'id': 4,
            'question': 'What is a HashMap and how does it work internally?',
            'keywords': ['key', 'value', 'hash', 'bucket', 'collision', 'array'],
            'max_score': 2
        },
        {
            'id': 5,
            'question': 'Explain the difference between abstract class and interface.',
            'keywords': ['implementation', 'multiple', 'methods', 'variables', 'extends', 'implements'],
            'max_score': 2
        }
    ],
    'qa': [
        {
            'id': 1,
            'question': 'What is the difference between functional and non-functional testing?',
            'keywords': ['behavior', 'performance', 'usability', 'security', 'what', 'how'],
            'max_score': 2
        },
        {
            'id': 2,
            'question': 'Explain the testing pyramid and its layers.',
            'keywords': ['unit', 'integration', 'e2e', 'end-to-end', 'speed', 'cost'],
            'max_score': 2
        },
        {
            'id': 3,
            'question': 'What is regression testing and when should it be performed?',
            'keywords': ['change', 'bug', 'fix', 'existing', 'verify', 'impact'],
            'max_score': 2
        },
        {
            'id': 4,
            'question': 'Explain the difference between black box and white box testing.',
            'keywords': ['internal', 'external', 'code', 'structure', 'input', 'output'],
            'max_score': 2
        },
        {
            'id': 5,
            'question': 'What is test-driven development (TDD)?',
            'keywords': ['test', 'first', 'code', 'refactor', 'cycle', 'fail'],
            'max_score': 2
        }
    ]
}

def calculate_technical_score(answers: dict, role: str) -> int:
    """Calculate technical score based on keyword matching (max 10)"""
    questions = TECHNICAL_QUESTIONS.get(role, TECHNICAL_QUESTIONS['python'])
    total_score = 0
    
    for question in questions:
        answer = answers.get(str(question['id']), '').lower()
        keywords = question['keywords']
        matched_keywords = sum(1 for keyword in keywords if keyword.lower() in answer)
        question_score = min(question['max_score'], matched_keywords)
        total_score += question_score
    
    return min(10, total_score)

def save_technical_answers(user_id: int, answers: dict, role: str, score: int):
    """Save technical answers to database"""
    db = get_db()
    try:
        for question_id, answer in answers.items():
            db.client.table('technical_answers').insert({
                'user_id': user_id,
                'question_id': int(question_id),
                'answer': answer,
                'score': 0
            }).execute()
        
        db.client.table('candidate_scores').update({'round3_score': score}).eq('user_id', user_id).execute()
        db.client.table('candidate_status').update({'current_round': 3}).eq('user_id', user_id).execute()
        return True
    except Exception as e:
        st.error(f"Error saving answers: {str(e)}")
        return False

def render_round3():
    """Render Round 3: Technical Evaluation"""
    st.markdown("""
        <div style="margin-bottom: 30px;">
            <h1 style="font-size: 32px; margin-bottom: 10px;">💻 Round 03: Technical Core</h1>
            <p style="color: rgba(255,255,255,0.6);">Analyzing your depth of knowledge in your specialized stack.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0) if user else 0
    user_id = user.get('id', 0)
    if not user_id: return
    
    role = st.selectbox(
        "SPECIALIZATION STACK:",
        ['python', 'java', 'qa'],
        format_func=lambda x: x.upper(),
        index=0
    )
    
    db = get_db()
    existing_answers = db.client.table('technical_answers').select('*').eq('user_id', user_id).execute()
    
    if existing_answers.data:
        scores = db.client.table('candidate_scores').select('*').eq('user_id', user_id).execute()
        score = scores.data[0].get('round3_score', 0) if scores.data else 0
        
        st.markdown(f"""
            <div class="clay-card" style="text-align: center;">
                <h2 style="color: var(--accent); margin-bottom: 20px;">TECHNICAL VERIFIED</h2>
                <div class="metric-value" style="font-size: 72px;">{score}/10</div>
                <p style="color: var(--text-secondary); margin-top: 10px;">Architecture and logic patterns indexed and scored.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        if st.button("PROCEED TO ALGORITHMIC CHALLENGE ⌨️", use_container_width=True, type="primary"):
            st.session_state.current_round = 3
            st.rerun()
    else:
        questions = TECHNICAL_QUESTIONS.get(role, TECHNICAL_QUESTIONS['python'])
        answers = {}
        
        for i, question in enumerate(questions):
            st.markdown(f"""
                <div class="glass-card" style="margin-bottom: 20px;">
                    <h4 style="color: rgba(255, 255, 255, 0.4); font-size: 12px;">CONCEPT {i+1}/05</h4>
                    <p style="font-size: 18px; margin-bottom: 20px;">{question['question']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            answer = st.text_area(
                f"Response Matrix {i+1}:",
                placeholder="Elaborate your technical understanding...",
                key=f"tech_q{question['id']}",
                height=150,
                label_visibility="collapsed"
            )
            answers[str(question['id'])] = answer
            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        
        if st.button("SUBMIT TECHNICAL CORE", use_container_width=True, type="primary"):
            score = calculate_technical_score(answers, role)
            if save_technical_answers(user_id, answers, role, score):
                st.balloons()
                st.rerun()
