"""
Anti-Cheating Module: Sidebar Gateway Edition
Premium UI (Landing Page Reference)
"""

import os
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
            st.sidebar.warning("⏳ Verification Required")

    if not st.session_state.get('proctoring_verified', False):
        st.markdown('<div style="height: 5vh;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto;">
                <h1 style="font-size: 36px; margin-bottom: 15px; background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">IDENTITY VERIFICATION</h1>
                <p style="font-size: 15px; color: rgba(255,255,255,0.6); margin-bottom: 25px;">
                    Please align your face within the pulsing target area below to authorize your session.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Dotted target circle styling
        st.markdown("""
            <style>
                .camera-wrapper {
                    position: relative;
                    width: 320px;
                    margin: 20px auto;
                    border-radius: 16px;
                    overflow: hidden;
                    border: 2px solid rgba(99, 102, 241, 0.3);
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
                }
                .target-circle {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 160px;
                    height: 160px;
                    border: 3px dashed #6366f1;
                    border-radius: 50%;
                    pointer-events: none;
                    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
                    z-index: 99;
                    animation: pulse 2s infinite alternate;
                }
                @keyframes pulse {
                    0% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.7; }
                    100% { transform: translate(-50%, -50%) scale(1.05); opacity: 1; }
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown('<div class="camera-wrapper"><div class="target-circle"></div>', unsafe_allow_html=True)
            img_file = st.camera_input("Verification Scanner", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if os.getenv("PLAYWRIGHT_TEST") == "1":
                if st.button("🧪 BYPASS FACE CHECK (TEST)", use_container_width=True):
                    st.session_state.proctoring_verified = True
                    st.rerun()
            
            if img_file is not None:
                image_bytes = img_file.getvalue()
                
                # Perform backend face detection using OpenCV
                from modules.security_core import analyze_frame_opencv
                analysis = analyze_frame_opencv(image_bytes)
                
                if analysis.get("person_count", 0) > 0:
                    st.success("✅ Face Detected! Identity Verified successfully.")
                    if st.button("PROCEED TO EXAM", use_container_width=True, type="primary"):
                        st.session_state.proctoring_verified = True
                        st.rerun()
                else:
                    st.error("❌ Face not detected. Please align your face inside the dotted circle and try again.")
            else:
                st.info("📸 Please snap a photo using the camera button to verify.")
        
        return False

    st.sidebar.markdown(f"""
        <div style="margin-top: 10px; padding: 15px; background: rgba(99, 102, 241, 0.05); border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <span style="font-size: 11px; color: #fff; font-weight: 700; opacity: 0.6;">SESSION SECURITY</span>
                <span style="font-size: 11px; color: #6366f1; font-weight: 800;">VERIFIED</span>
            </div>
            <div style="font-size: 10px; color: rgba(255,255,255,0.4);">Tab switches: {st.session_state.tab_switch_count}/{st.session_state.max_tab_switches}</div>
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
