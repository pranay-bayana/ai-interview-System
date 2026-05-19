"""
Anti-Cheating Module: Sidebar Gateway Edition
Premium UI (Landing Page Reference)
"""

import streamlit as st
import streamlit.components.v1 as components
from database.init_db import get_db
from streamlit_javascript import st_javascript
from modules.security_core import run_security_checks

def init_anticheat_state():
    if 'tab_switch_count' not in st.session_state:
        st.session_state.tab_switch_count = 0
    if 'max_tab_switches' not in st.session_state:
        st.session_state.max_tab_switches = 5
    if 'cheating_detected' not in st.session_state:
        st.session_state.cheating_detected = False
    if 'cheating_reason' not in st.session_state:
        st.session_state.cheating_reason = ""
    if 'proctoring_verified' not in st.session_state:
        st.session_state.proctoring_verified = False

def render_sidebar_security():
    """Render the sidebar camera and verification button (Indigo Style)"""
    st.sidebar.markdown('<div style="font-size: 11px; font-weight: 700; color: #6366f1; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px;">AI Proctoring Sidebar</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        components.html("""
            <div id="cam-box" style="width: 100%; border-radius: 12px; overflow: hidden; background: #000; aspect-ratio: 16/9; position: relative; border: 1px solid rgba(99, 102, 241, 0.2);">
                <video id="v" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1);"></video>
                <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; background: #6366f1; box-shadow: 0 0 10px #6366f1; animation: scan 3s linear infinite;"></div>
            </div>
            <style>@keyframes scan { 0% { bottom: 0; } 50% { bottom: 100%; } 100% { bottom: 0; } }</style>
            <script>
                async function init() {
                    const v = document.getElementById('v');
                    try {
                        const s = await navigator.mediaDevices.getUserMedia({ video: true });
                        v.srcObject = s;
                    } catch(e) { console.error(e); }
                }
                init();
            </script>
        """, height=160)

        if not st.session_state.get('proctoring_verified', False):
            if st.button("🔐 VERIFY IDENTITY", use_container_width=True, type="primary", key="sidebar_verify_btn"):
                st.session_state.proctoring_verified = True
                st.rerun()

    if not st.session_state.get('proctoring_verified', False):
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h1 style="font-size: 42px; margin-bottom: 25px;">IDENTITY VERIFICATION</h1>
                <p style="font-size: 18px; color: rgba(255,255,255,0.6); max-width: 600px; margin: 0 auto 40px auto;">
                    To maintain the integrity of the neural assessment, please verify your identity via the sidebar camera.
                </p>
                <div style="padding: 20px; border-radius: 12px; background: rgba(99, 102, 241, 0.05); border: 1px dashed var(--primary); display: inline-block;">
                    <span style="color: var(--primary); font-weight: 700;">STATUS: WAITING FOR SECURE LINK...</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return False

    st.sidebar.markdown(f"""
        <div style="margin-top: 10px; padding: 15px; background: rgba(99, 102, 241, 0.05); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <span style="font-size: 11px; color: #fff; font-weight: 700; opacity: 0.6;">SESSION SECURITY</span>
                <span style="font-size: 11px; color: #6366f1; font-weight: 800;">VERIFIED</span>
            </div>
            <div style="font-size: 10px; color: rgba(255,255,255,0.4);">Violations: {st.session_state.tab_switch_count}/{st.session_state.max_tab_switches}</div>
        </div>
    """, unsafe_allow_html=True)
    return True

def render_anticheat_panel(round_number: int):
    init_anticheat_state()
    if st.session_state.get('cheating_detected', False):
        st.error(f"🚨 DISQUALIFIED: {st.session_state.cheating_reason}")
        return False
    
    verified = render_sidebar_security()
    if not verified: return False
    
    allow_tab_switch = (round_number == 0)
    
    # Run core security guards
    if not run_security_checks(allow_tab_switch=allow_tab_switch):
        st.markdown("""
            <div class="glass-card" style="border: 2px solid #ff4b4b; background: rgba(255, 75, 75, 0.05); text-align: center; padding: 50px; margin-top: 20px;">
                <h1 style="color: #ff4b4b; margin-bottom: 20px; font-size: 36px;">🚨 SESSION DISQUALIFIED</h1>
                <p style="font-size: 18px; color: #fff; max-width: 600px; margin: 0 auto 30px auto; line-height: 1.6;">
                    This interview session has been terminated due to multiple security violations (such as repeated tab switching or losing browser focus).
                </p>
                <div style="padding: 15px 25px; background: rgba(255,255,255,0.05); border-radius: 12px; font-size: 14px; color: rgba(255,255,255,0.6); display: inline-block;">
                    All security events have been synced to the Administrator Control Center.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return False
    
    return True
