"""
Round 6: AI Chatbot Module
World-Class Neural Assistant with Robust Fallback Intelligence
"""

import streamlit as st
from database.init_db import get_db
from openai import OpenAI
import os

# Local Intelligence Database for Offline Mode
OFFLINE_KNOWLEDGE = {
    "jdbc": "JDBC (Java Database Connectivity) is a Java API that manages connecting to a database, issuing queries and commands, and handling result sets. It acts as a bridge between your Java application and various databases like MySQL, PostgreSQL, or Oracle.",
    "java": "Java is a high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It is famous for its 'Write Once, Run Anywhere' capability.",
    "python": "Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation.",
    "react": "React is a free and open-source front-end JavaScript library for building user interfaces based on UI components. It is maintained by Meta and a community of individual developers and companies.",
    "sql": "SQL (Structured Query Language) is a domain-specific language used in programming and designed for managing data held in a relational database management system.",
    "api": "An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other.",
    "tip": "Always research the company's recent projects and values before the interview. It shows genuine interest and initiative.",
    "confidence": "Maintain a steady breathing rhythm and pause for 2 seconds before answering complex questions. This projects intelligence and control."
}

def get_ai_response(messages):
    """Get intelligent response with robust fallback"""
    user_msg = messages[-1]['content'].lower()
    
    # Try OpenAI first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and "your_key" not in api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a professional AI Recruitment Assistant."}] + messages,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception:
            pass # Fallback to local intelligence
            
    # Local Intelligence Fallback
    for key, value in OFFLINE_KNOWLEDGE.items():
        if key in user_msg:
            return f"[Neural Local Intel]: {value} Is there anything else you would like to know about {key} or related technologies?"
            
    return "[Neural Assistant]: I am currently analyzing your query. For the best experience, ensure your OPENAI_API_KEY is configured. In the meantime, I can assist with Java, Python, SQL, React, and general interview strategies. What else is on your mind?"

def render_round6():
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 44px; margin-bottom: 12px; font-weight: 900;">🤖 Round 06: Neural Assistant</h1>
            <p style="color: var(--text-secondary); font-size: 20px;">Real-time strategic briefing and cognitive performance optimization.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.get('user', {})
    user_id = user.get('id', 0)
    if not user_id: return

    # Initialize Chat History
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Neural Core synchronized. I am your strategic assistant. Ask me anything about your technical interview, company research, or confidence metrics."}
        ]

    # Persistent Chat Container
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_messages:
            is_user = msg['role'] == 'user'
            align = "flex-end" if is_user else "flex-start"
            bg = "linear-gradient(135deg, #6366f1, #a855f7)" if is_user else "rgba(255,255,255,0.05)"
            glow = "0 0 15px rgba(99, 102, 241, 0.4)" if is_user else "none"
            
            st.markdown(f"""
                <div style="display: flex; justify-content: {align}; margin-bottom: 20px;">
                    <div class="clay-card" style="padding: 15px 25px; max-width: 75%; background: {bg}; 
                                border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); 
                                box-shadow: {glow}; position: relative;">
                        <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 5px; font-weight: 800;">
                            { 'CANDIDATE' if is_user else 'NEURAL_CORE' }
                        </div>
                        <div style="font-size: 16px; line-height: 1.5;">{msg["content"]}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input("TRANSMIT COMMAND..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Decoding neural vectors..."):
            ai_resp = get_ai_response(st.session_state.chat_messages)
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_resp})
        
        st.rerun()

    # Completion Button
    if len(st.session_state.chat_messages) > 1:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        if st.button("🏁 FINALIZE STRATEGIC BRIEFING", use_container_width=True):
            db = get_db()
            db.client.table('candidate_scores').update({'round6_score': 10}).eq('user_id', user_id).execute()
            db.client.table('candidate_status').update({'current_round': 6}).eq('user_id', user_id).execute()
            st.session_state.current_round = 6
            st.rerun()
