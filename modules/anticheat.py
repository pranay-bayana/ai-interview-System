"""
Anti-Cheating Module for AI Recruitment Ecosystem
Features: Multi-face detection, tab switching detection, fullscreen enforcement
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
from database.init_db import get_db
from streamlit_javascript import st_javascript

# Initialize session state for anti-cheating
def init_anticheat_state():
    """Initialize anti-cheating session state"""
    if 'tab_switch_count' not in st.session_state:
        st.session_state.tab_switch_count = 0
    if 'max_tab_switches' not in st.session_state:
        st.session_state.max_tab_switches = 3
    if 'cheating_detected' not in st.session_state:
        st.session_state.cheating_detected = False
    if 'cheating_reason' not in st.session_state:
        st.session_state.cheating_reason = ""
    if 'anticheat_warnings' not in st.session_state:
        st.session_state.anticheat_warnings = 0
    if 'last_visibility_state' not in st.session_state:
        st.session_state.last_visibility_state = "visible"

def detect_faces(image: np.ndarray) -> int:
    """Detect number of faces in image using OpenCV"""
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        return len(faces)
    except Exception:
        return 0

def render_face_detection_monitor():
    """Render face detection monitoring component"""
    with st.expander("👁️ Security Monitor", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            camera_image = st.camera_input("Verify Identity", key="face_camera", label_visibility="collapsed")
        
        with col2:
            st.markdown("""
                <div style="padding: 10px; background: rgba(255, 107, 107, 0.1); border-radius: 10px; border: 1px solid rgba(255, 107, 107, 0.2);">
                    <p style="font-size: 12px; margin-bottom: 5px; color: #ff6b6b; font-weight: 700;">SECURITY PROTOCOL ACTIVE</p>
                    <p style="font-size: 11px; margin-bottom: 0; color: rgba(255,255,255,0.6);">
                        • Ensure clear lighting<br/>
                        • No other persons allowed<br/>
                        • Maintain eye contact with screen
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if camera_image:
                image_bytes = camera_image.read()
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                num_faces = detect_faces(image)
                
                if num_faces == 0:
                    st.error("No face detected!")
                elif num_faces == 1:
                    st.success("Identity Verified")
                else:
                    st.error(f"Multiple faces detected!")
                    record_cheating_violation("Multiple faces detected")

def render_tab_switching_detection(allow_switching: bool = False):
    """Detect tab switching using JavaScript"""
    if allow_switching:
        return
    
    # JS to check visibility state
    visibility_state = st_javascript("document.visibilityState")
    
    if visibility_state == "hidden" and st.session_state.last_visibility_state == "visible":
        st.session_state.tab_switch_count += 1
        st.session_state.last_visibility_state = "hidden"
        st.toast(f"⚠️ Warning: Tab switch detected ({st.session_state.tab_switch_count}/{st.session_state.max_tab_switches})", icon="🚨")
        
        if st.session_state.tab_switch_count >= st.session_state.max_tab_switches:
            record_cheating_violation("Exceeded tab switching limit")
            
    elif visibility_state == "visible":
        st.session_state.last_visibility_state = "visible"

def record_cheating_violation(reason: str):
    """Record cheating violation in database and update state"""
    user = st.session_state.get('user')
    user_id = user.get('id', 0) if user else 0
    if not user:
        return
    
    if not st.session_state.cheating_detected:
        st.session_state.cheating_detected = True
        st.session_state.cheating_reason = reason
        
        db = get_db()
        try:
            # Log violation
            db.client.table('anticheat_violations').insert({
                'user_id': user_id,
                'violation_type': reason,
                'round_number': st.session_state.current_round + 1
            }).execute()
            
            # Update status to rejected
            db.client.table('candidate_status').update({
                'status': 'rejected',
                'feedback': f"DISQUALIFIED: {reason}"
            }).eq('user_id', user_id).execute()
        except Exception:
            pass

def render_anticheat_panel(round_number: int):
    """Main entry point for anti-cheating measures"""
    init_anticheat_state()
    
    if st.session_state.cheating_detected:
        st.markdown(f"""
            <div class="glass-card" style="border-color: #ff6b6b; background: rgba(255, 107, 107, 0.05);">
                <h2 style="color: #ff6b6b; margin-bottom: 10px;">⚠️ DISQUALIFIED</h2>
                <p>Your session has been terminated due to security violations.</p>
                <p style="font-size: 14px; font-weight: 700;">Reason: {st.session_state.cheating_reason}</p>
                <hr style="border-color: rgba(255, 107, 107, 0.2);"/>
                <p style="font-size: 12px; color: rgba(255,255,255,0.5);">Please contact the recruitment administrator for further assistance.</p>
            </div>
        """, unsafe_allow_html=True)
        return False
    
    # Tab switching logic
    allow_tab_switch = (round_number == 1) # Allowed for resume upload
    render_tab_switching_detection(allow_switching=allow_tab_switch)
    
    # Face detection for technical rounds (2-5)
    if 2 <= round_number <= 5:
        render_face_detection_monitor()
        
    return True
