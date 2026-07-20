"""
Unified Security & Proctoring Core (Reconstructed Phase)
"""

import os
import time
import base64
import json
try:
    import cv2
except ImportError:
    cv2 = None
import numpy as np
import requests
import streamlit as st
import streamlit.components.v1 as components
from database.init_db import get_db

# --- Constants & Config ---
MAX_TAB_SWITCHES = 5  
MAX_VIOLATIONS = 5 
REQUIRE_FULLSCREEN = True
PROCTOR_INTERVAL_SEC = 15.0 # Standard proctoring frequency
AI_ANALYSIS_INTERVAL = 15.0 # Balanced AI checks

def is_e2e_bypass() -> bool:
    return os.getenv("E2E_BYPASS_SECURITY", "0").lower() in ("1", "true", "yes")

# --- Violation Logging ---
def log_violation(reason: str, severity: str = "high"):
    if "security_violations" not in st.session_state:
        st.session_state.security_violations = []
    
    violation = {
        "timestamp": time.strftime("%H:%M:%S"),
        "reason": reason,
        "severity": severity,
        "round": st.session_state.get("current_round", 0)
    }
    st.session_state.security_violations.append(violation)
    
    # Update DB
    user = st.session_state.get("user")
    if user:
        try:
            db = get_db()
            db.client.table("security_logs").insert({
                "user_id": user.get("id"),
                "violation_type": reason,
                "severity": severity,
                "details": f"Round: {violation['round']}"
            }).execute()
        except Exception:
            pass

def is_disqualified() -> bool:
    if st.session_state.get("security_disqualified", False):
        return True
    
    violations = len(st.session_state.get("security_violations", []))
    switches = st.session_state.get("tab_switch_count", 0)
    
    if violations >= MAX_VIOLATIONS or switches >= MAX_TAB_SWITCHES:
        st.session_state.security_disqualified = True
        return True
    return False

# --- Vision Intelligence ---

def analyze_frame_opencv(image_bytes: bytes) -> dict:
    if cv2 is None:
        return {"person_count": 0, "electronic_devices_detected": False, "ok": False, "engine": "opencv-fallback-disabled"}
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return {"person_count": 0, "electronic_devices_detected": False, "ok": False}

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frontal = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        profile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
        
        # Moderate detection (Sweet spot)
        faces_front = frontal.detectMultiScale(gray, 1.2, 6, minSize=(40, 40))
        faces_prof = profile.detectMultiScale(gray, 1.2, 6, minSize=(40, 40))
        
        # Combine (approximate unique faces)
        count = len(faces_front) + len(faces_prof)
        
        return {
            "person_count": count,
            "electronic_devices_detected": False,
            "ok": True,
            "engine": "opencv-enhanced",
        }
    except Exception:
        return {"person_count": 0, "electronic_devices_detected": False, "ok": False}

def analyze_frame_ollama(image_bytes: bytes) -> dict:
    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": (
                    "CRITICAL SECURITY AUDIT: Search for any mobile phone, smartphone, or tablet in this image. "
                    "First, describe what the person is holding. "
                    "Second, output 'PHONE_FOUND: TRUE' or 'PHONE_FOUND: FALSE'. "
                    "Even a partially visible screen counts as TRUE."
                ),
                "images": [b64],
                "stream": False,
            },
            timeout=15,
        )
        if response.status_code == 200:
            res_text = response.json().get("response", "").upper()
            # LOG TO TERMINAL FOR DEBUGGING
            print(f"--- AI SECURITY SCAN ---")
            print(f"RAW RESPONSE: {res_text}")
            
            # Robust fuzzy parsing
            phone_detected = False
            if "PHONE_FOUND: TRUE" in res_text or "PHONE_FOUND:TRUE" in res_text:
                phone_detected = True
            elif "TRUE" in res_text and any(k in res_text for k in ["PHONE", "MOBILE", "DEVICE", "SMARTPHONE"]):
                phone_detected = True
            elif any(k in res_text for k in ["SMARTPHONE", "MOBILE PHONE", "CELL PHONE"]) and "NO " not in res_text:
                phone_detected = True

            st.session_state.last_ai_thought = res_text # Store for sidebar display

            data = {
                "phone_detected": phone_detected,
                "ok": True,
                "engine": "ollama-high-res-audit"
            }
            print(f"PARSED DATA: {data}")
            return data
        elif response.status_code == 404:
             st.sidebar.error("⚠️ AI Vision Model (llava) not found. Run 'ollama pull llava' in terminal.")
    except Exception:
        pass
    return None

def analyze_proctor_frame(image_bytes: bytes) -> dict:
    if st.session_state.get("ai_proctor_busy", False):
        return {"ok": False, "msg": "Analysis in progress"}
    
    st.session_state.ai_proctor_busy = True
    try:
        now = time.time()
        last_ai = st.session_state.get("last_proctor_check", 0)
        
        # Fast path: OpenCV (always run)
        opencv = analyze_frame_opencv(image_bytes)
        
        # Heavy path: Ollama (run faster during verification)
        interval = 5.0 if not st.session_state.get("proctoring_verified", False) else AI_ANALYSIS_INTERVAL
        if (now - last_ai) > interval:
            st.session_state.last_proctor_check = now
            ollama = analyze_frame_ollama(image_bytes)
            if ollama and ollama.get("ok"):
                # CONSENSUS LOGIC: Trust AI count primarily for 1+ person
                ai_count = ollama.get("person_count", 0)
                cv_count = opencv.get("person_count", 0)
                
                if ai_count >= 1:
                    final_count = ai_count
                else:
                    final_count = cv_count

                st.session_state.last_known_person_count = final_count

                opencv.update({
                    "person_count": final_count,
                    "phone_detected": ollama.get("phone_detected", False),
                    "engine": "hybrid-vision-ai-primary"
                })
        else:
            # Between AI runs, use memory if OpenCV is currently failing
            cached_count = st.session_state.get("last_known_person_count", 0)
            if opencv.get("person_count", 0) == 0 and cached_count > 0:
                opencv["person_count"] = cached_count
                opencv["engine"] = "hybrid-vision-memory"
        
        return opencv
    finally:
        st.session_state.ai_proctor_busy = False

def evaluate_proctor_frame(image_bytes: bytes) -> list[str]:
    analysis = analyze_proctor_frame(image_bytes)
    violations = []
    
    # FACE DETECTION DISABLED PER USER REQUEST
    # Only monitoring for electronic devices now
    
    if analysis.get("middle_finger_detected"):
        violations.append("Offensive Gesture: Middle finger detected")

    if analysis.get("phone_detected"):
        violations.append("Security Violation: Electronic device (Phone/Tablet) detected in frame")
        
    return violations

# --- Browser Guards ---

def inject_browser_guards():
    """Block copy/paste and context menu inside the Streamlit parent document."""
    js_code = r"""
        <script>
        (function () {
            const parentDoc = window.parent.document;
            const parentWin = window.parent;
            
            // Ultra-robust button search that ignores case, spaces, icons, and HTML wrappers
            const findButtonByText = (text) => {
                try {
                    const allButtons = Array.from(parentDoc.querySelectorAll('button'));
                    const target = text.toLowerCase().replace(/[\s_]/g, '');
                    for (let btn of allButtons) {
                        const content = (btn.innerText || btn.textContent || '').toLowerCase().replace(/[\s_]/g, '');
                        if (content.includes(target)) {
                            return btn;
                        }
                    }
                } catch(e) { console.error("Error finding button:", e); }
                return null;
            };

            // Ultimate multi-method click dispatch to completely bypass browser & framework blocks
            const forceClick = (btn) => {
                if (!btn) return false;
                try {
                    btn.click();
                } catch(e) {}
                try {
                    const clickEvent = new MouseEvent('click', {
                        view: parentWin,
                        bubbles: true,
                        cancelable: true
                    });
                    btn.dispatchEvent(clickEvent);
                } catch(e) {}
                return true;
            };

            // Clear any stale flags from previous unmonitored sessions on load
            localStorage.removeItem('pending_tab_switch');

            // --- SECURE PROCTORING SINGLETON SCRIPT INJECTION ---
            const triggerPendingActions = () => {
                if (localStorage.getItem('pending_tab_switch') === 'true') {
                    const btn = findButtonByText("hidden_tab_trigger");
                    if (btn) {
                        localStorage.removeItem('pending_tab_switch');
                        forceClick(btn);
                    }
                }
            };

            // Clean up previous event listeners if they exist to prevent dead object references
            if (parentWin.__activeVisibilityListener) {
                try {
                    parentDoc.removeEventListener('visibilitychange', parentWin.__activeVisibilityListener, true);
                    document.removeEventListener('visibilitychange', parentWin.__activeVisibilityListener, true);
                } catch(e) {}
            }
            if (parentWin.__activeFocusListener) {
                try {
                    parentWin.removeEventListener('focus', parentWin.__activeFocusListener, true);
                } catch(e) {}
            }

            // Define handlers
            const handleVisibilityChange = () => {
                if (parentDoc.visibilityState === 'hidden' || document.visibilityState === 'hidden') {
                    console.warn("⚠️ SECURE AGENT: Visibility Hidden Detected!");
                    localStorage.setItem('pending_tab_switch', 'true');
                } else if (parentDoc.visibilityState === 'visible' && document.visibilityState === 'visible') {
                    triggerPendingActions();
                }
            };

            // Save reference and attach fresh listeners
            parentWin.__activeVisibilityListener = handleVisibilityChange;
            parentWin.__activeFocusListener = triggerPendingActions;

            try {
                parentDoc.addEventListener('visibilitychange', handleVisibilityChange, true);
                document.addEventListener('visibilitychange', handleVisibilityChange, true);
                parentWin.addEventListener('focus', triggerPendingActions, true);
                console.log("🔒 JEE-MAINS SECURE PROCTORING ACTIVE WITH LIVING CONTEXT!");
                // Trigger any pending actions immediately on load
                triggerPendingActions();
            } catch(e) { console.error("Error launching secure agent:", e); }

            // Re-install keyboard and copy blocks
            const block = (e) => { 
                e.preventDefault(); 
                e.stopPropagation(); 
                return false; 
            };
            
            // Clean up keyboard blocks on parent doc if previously installed
            if (parentWin.__blockHandler) {
                try {
                    ['copy', 'cut', 'paste', 'contextmenu', 'dragstart', 'drop'].forEach((evt) => {
                        parentDoc.removeEventListener(evt, parentWin.__blockHandler, true);
                    });
                    parentDoc.removeEventListener('keydown', parentWin.__keydownHandler, true);
                } catch(e) {}
            }

            const keydownHandler = (e) => {
                if (e.key === 'PrintScreen' || e.keyCode === 123) {
                    return block(e);
                }
                if ((e.ctrlKey || e.metaKey) && ['c','v','x','a','p','s','u'].includes(e.key.toLowerCase())) {
                    e.preventDefault();
                }
            };

            parentWin.__blockHandler = block;
            parentWin.__keydownHandler = keydownHandler;

            ['copy', 'cut', 'paste', 'contextmenu', 'dragstart', 'drop'].forEach((evt) => {
                parentDoc.addEventListener(evt, block, true);
            });
            parentDoc.addEventListener('keydown', keydownHandler, true);

            // Reliable trigger hiding
            const hideTriggers = () => {
                const buttons = Array.from(parentDoc.querySelectorAll('button'));
                buttons.forEach(btn => {
                    const txt = btn.textContent || "";
                    if (txt.includes("hidden_tab_trigger") || 
                        txt.includes("hidden_devtools_trigger") ||
                        txt.includes("hidden_proctor_trigger")) {
                        
                        const container = btn.closest('div[data-testid="stButton"]');
                        if (container) {
                            container.style.position = 'absolute';
                            container.style.width = '1px';
                            container.style.height = '1px';
                            container.style.padding = '0';
                            container.style.margin = '-1px';
                            container.style.overflow = 'hidden';
                            container.style.clip = 'rect(0, 0, 0, 0)';
                            container.style.border = '0';
                            container.style.opacity = '0.01';
                        }
                    }
                });
            };
            hideTriggers();
            setInterval(hideTriggers, 500);
        })();
        </script>
    """
    components.html(f"<!-- Cache Buster: {time.time()} -->\n" + js_code, height=2)


def render_security_sidebar():
    if is_e2e_bypass():
        return
    
    violations = len(st.session_state.get("security_violations", []))
    switches = st.session_state.get("tab_switch_count", 0)
    verified_label = "✅ SECURED" if st.session_state.proctoring_verified else "⏳ PENDING"
    verified_color = "#43e97b" if st.session_state.proctoring_verified else "#ffb347"

    st.sidebar.markdown(
        f"""
        <div class="security-panel">
            <div class="security-panel-title">Live proctoring</div>
            <div class="security-stat"><span>Status</span><strong class="{'ok' if not is_disqualified() else 'bad'}">
                {'ACTIVE' if not is_disqualified() else 'TERMINATED'}</strong></div>
            <div class="security-stat"><span>Tab switches</span><strong>{switches}/{MAX_TAB_SWITCHES}</strong></div>
            <div class="security-stat"><span>Identity check</span><strong style="color: {verified_color};">{verified_label}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # AI Thought Log (Small and discrete)
    if st.session_state.get("last_ai_thought"):
        with st.sidebar.expander("👁️ AI Vision Log", expanded=False):
            st.caption(f"Last Scan: {st.session_state.last_ai_thought}")

    if violations > 0 or switches > 0:
        st.sidebar.markdown("### 🚨 Recent Violations")
        for v in st.session_state.get("security_violations", []):
            st.sidebar.error(v["reason"], icon="⚠️")
        
        if st.sidebar.button("🔄 RESET SECURITY", use_container_width=True):
            st.session_state.security_violations = []
            st.session_state.tab_switch_count = 0
            st.session_state.security_disqualified = False
            st.session_state.proctoring_verified = False
            st.rerun()

def run_security_checks(allow_tab_switch: bool = False) -> bool:
    if is_e2e_bypass():
        return True
    
    if "tab_switch_count" not in st.session_state:
        st.session_state.tab_switch_count = 0

    inject_browser_guards()

    # Hidden triggers for JS to click
    if st.button("hidden_tab_trigger"):
        if not allow_tab_switch:
            st.session_state.tab_switch_count += 1
            log_violation("Critical: Tab Switch Detected (Visibility Hidden)")
            st.rerun()

    # The live camera in the sidebar now handles all background proctoring.

    with st.sidebar:
        render_security_sidebar()
    
    return not is_disqualified()
