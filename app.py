"""
AI-Powered Recruitment Ecosystem
Main Application File - Hyper-Futuristic Holographic Edition
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Recruitment Ecosystem",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Holographic UI
def load_holographic_ui():
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
            # Neural Matrix Grid & Animated Orbs
            st.markdown("""
                <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: -1; overflow: hidden;">
                    <div style="position: absolute; width: 100%; height: 100%; background-image: radial-gradient(circle at 1px 1px, rgba(0, 242, 255, 0.05) 1px, transparent 0); background-size: 60px 60px;"></div>
                    <div class="holographic-glow" style="position: absolute; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(112, 0, 255, 0.05) 0%, transparent 70%);"></div>
                </div>
            """, unsafe_allow_html=True)

load_holographic_ui()

# Session state
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user' not in st.session_state: st.session_state.user = None
if 'current_round' not in st.session_state: st.session_state.current_round = 0

# Import modules
from modules.auth import render_auth_page, render_admin_access, check_auth, get_current_user, logout
from modules.admin import render_admin_dashboard
from modules.round1_resume import render_round1
from modules.round2_aptitude import render_round2
from modules.round3_technical import render_round3
from modules.round4_coding import render_round4
from modules.round5_voice import render_round5
from modules.round6_chatbot import render_round6
from modules.round7_dashboard import render_round7
from modules.anticheat import render_anticheat_panel

def render_home():
    st.markdown("""
        <div style="text-align: center; padding: 150px 20px;">
            <div style="display: inline-block; padding: 10px 30px; background: rgba(0, 242, 255, 0.05); 
                        border: 1px solid var(--primary); border-radius: 50px; margin-bottom: 30px; 
                        font-family: 'Syncopate'; font-size: 10px; letter-spacing: 5px; color: var(--primary);">
                AI RECRUITMENT SYSTEM
            </div>
            <h1 style="font-size: 96px; margin-bottom: 20px;">
                NEURAL CORE
            </h1>
            <p style="font-size: 20px; color: #94a3b8; max-width: 800px; margin: 0 auto 60px auto; 
                       font-family: 'Outfit'; letter-spacing: 2px; text-transform: uppercase;">
                Quantum Skill Mapping • Automated Intelligence • Elite Selection
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("INITIATE UPLINK ⚡", use_container_width=True):
            st.session_state.current_page = 'auth'
            st.rerun()

def main():
    # Sidebar
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 40px 0;">
            <div style="font-size: 72px; margin-bottom: 20px; filter: drop-shadow(0 0 25px #00f2ff);">🎯</div>
            <h2 style="font-family: 'Syncopate'; font-size: 18px; letter-spacing: 5px; color: white;">AI RECRUITMENT SYSTEM</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if check_auth():
        user = get_current_user() or {'full_name': 'USER', 'id': 'N/A'}
        st.sidebar.markdown(f"""
            <div style="background: rgba(0, 242, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.1); 
                        padding: 25px; border-radius: 24px; margin-bottom: 30px; text-align: center;">
                <p style="margin: 0; font-size: 16px; font-weight: 800; color: #00f2ff;">{user.get('full_name', 'USER')}</p>
                <div style="height: 1px; width: 30px; background: #00f2ff; margin: 15px auto;"></div>
                <p style="margin: 0; font-size: 9px; color: rgba(255,255,255,0.5); letter-spacing: 2px;">{ 'ADMIN_CORE_ACTIVE' if st.session_state.get('is_admin') else 'CANDIDATE_ACCESS_GRANTED' }</p>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.get('is_admin', False):
            rounds = [(0,"📄","RESUME"), (1,"🧠","APTITUDE"), (2,"💻","TECHNICAL"), (3,"⌨️","CODING"), (4,"🎙️","VOICE"), (5,"🤖","CHATBOT"), (6,"📊","DASHBOARD")]
            for i, icon, name in rounds:
                is_active = st.session_state.current_round == i
                if st.sidebar.button(f"{icon} {name}", use_container_width=True, key=f"nav_{name}", type="primary" if is_active else "secondary"):
                    st.session_state.current_round = i
                    st.rerun()
        
        st.sidebar.markdown("---")
        if st.sidebar.button("TERMINATE UPLINK", use_container_width=True):
            logout()
    else:
        st.sidebar.markdown("### SYSTEM_AUTH")
        if st.sidebar.button("🔐 AUTHENTICATE", use_container_width=True):
            st.session_state.current_page = 'auth'
            st.rerun()
        if st.sidebar.button("🎯 ADMIN_CORE", use_container_width=True):
            st.session_state.current_page = 'admin_access'
            st.rerun()

    # Page Routing
    if not check_auth():
        if st.session_state.get('current_page') == 'admin_access': render_admin_access()
        elif st.session_state.get('current_page') == 'auth': render_auth_page()
        else: render_home()
    else:
        if st.session_state.get('is_admin') and st.session_state.get('admin_verified'):
            render_admin_dashboard()
        else:
            curr = st.session_state.current_round
            if render_anticheat_panel(curr + 1):
                if curr == 0: render_round1()
                elif curr == 1: render_round2()
                elif curr == 2: render_round3()
                elif curr == 3: render_round4()
                elif curr == 4: render_round5()
                elif curr == 5: render_round6()
                elif curr == 6: render_round7()
                
                if curr < 6:
                    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
                    if st.button("NEXT_STAGE_PROCEED ⏩", use_container_width=True):
                        st.session_state.current_round += 1
                        st.rerun()

if __name__ == "__main__":
    main()
