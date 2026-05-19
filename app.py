"""
Main Application Entry Point for AI Recruitment Ecosystem
Ultra-Premium UI (Synchronized with Landing Page Reference)
"""

import streamlit as st
import os
from database.init_db import get_db
from modules.auth import render_auth_page
from modules.round1_resume import render_round1
from modules.round2_aptitude import render_round2
from modules.round3_technical import render_round3
from modules.round4_coding import render_round4
from modules.round5_voice import render_round5
from modules.round6_chatbot import render_round6
from modules.round7_dashboard import render_round7
from modules.anticheat import render_anticheat_panel

# Set page configuration
st.set_page_config(
    page_title="Interviewer.AI | Neural Ecosystem",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Database
get_db()

def load_synchronized_ui():
    """Inject Design Tokens from frontend_landing.html"""
    css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Advanced Background Orbs & Space (From 1215-line Reference)
    st.components.v1.html(
        """
        <script>
            const parentDoc = window.parent.document;
            
            // Prevent multiple injections
            if (!parentDoc.getElementById('space-canvas')) {
                const styles = `
                    #custom-cursor { position: fixed; width: 12px; height: 12px; background: #6366f1; border-radius: 50%; pointer-events: none; z-index: 9999; transform: translate(-50%, -50%); transition: transform 0.15s ease, background 0.3s ease; }
                    #custom-cursor-ring { position: fixed; width: 40px; height: 40px; border: 1.5px solid rgba(99,102,241,0.5); border-radius: 50%; pointer-events: none; z-index: 9998; transform: translate(-50%, -50%); transition: transform 0.4s cubic-bezier(.25,.46,.45,.94), width 0.3s, height 0.3s, border-color 0.3s; }
                    .bg-orb { position: fixed; border-radius: 50%; filter: blur(120px); pointer-events: none; z-index: 0; }
                    #orb1 { width: 700px; height: 700px; background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%); top: -200px; left: -200px; }
                    #orb2 { width: 600px; height: 600px; background: radial-gradient(circle, rgba(168,85,247,0.15) 0%, transparent 70%); top: 30%; right: -150px; }
                    #orb3 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(34,211,238,0.12) 0%, transparent 70%); bottom: 10%; left: 20%; }
                    #space-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
                `;
                
                const styleEl = parentDoc.createElement('style');
                styleEl.innerHTML = styles;
                parentDoc.head.appendChild(styleEl);

                const canvas = parentDoc.createElement('canvas');
                canvas.id = 'space-canvas';
                parentDoc.body.prepend(canvas);

                const orb1 = parentDoc.createElement('div'); orb1.className = 'bg-orb'; orb1.id = 'orb1'; parentDoc.body.prepend(orb1);
                const orb2 = parentDoc.createElement('div'); orb2.className = 'bg-orb'; orb2.id = 'orb2'; parentDoc.body.prepend(orb2);
                const orb3 = parentDoc.createElement('div'); orb3.className = 'bg-orb'; orb3.id = 'orb3'; parentDoc.body.prepend(orb3);

                const cursor = parentDoc.createElement('div'); cursor.id = 'custom-cursor'; parentDoc.body.appendChild(cursor);
                const ring = parentDoc.createElement('div'); ring.id = 'custom-cursor-ring'; parentDoc.body.appendChild(ring);

                let mx = 0, my = 0, rx = 0, ry = 0;
                parentDoc.addEventListener('mousemove', e => {
                    mx = e.clientX; my = e.clientY;
                    cursor.style.left = mx + 'px'; cursor.style.top = my + 'px';
                });
                
                function lerp() {
                    rx += (mx - rx) * 0.15; ry += (my - ry) * 0.15;
                    ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
                    requestAnimationFrame(lerp);
                }
                lerp();

                const ctx = canvas.getContext('2d');
                let W = window.parent.innerWidth;
                let H = window.parent.innerHeight;
                canvas.width = W; canvas.height = H;
                let stars = [];
                for(let i=0; i<180; i++) stars.push({x:Math.random()*W, y:Math.random()*H, r:Math.random()*1.2, o:Math.random(), s:Math.random()*0.15});
                
                function draw() {
                    ctx.clearRect(0,0,W,H);
                    stars.forEach(s => {
                        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
                        ctx.fillStyle = `rgba(255, 255, 255, ${s.o})`; ctx.fill();
                        s.y -= s.s; if(s.y<0) s.y=H;
                    });
                    requestAnimationFrame(draw);
                }
                window.parent.addEventListener('resize', () => { 
                    W = window.parent.innerWidth; H = window.parent.innerHeight;
                    canvas.width = W; canvas.height = H; 
                });
                draw();
            }
        </script>
        """,
        height=2,
    )

load_synchronized_ui()

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 0

    if not st.session_state.authenticated:
        st.markdown('<div style="height: 12vh;"></div>', unsafe_allow_html=True)
        render_auth_page()
    else:
        # Sidebar Branding (Sync with Landing Page Logo)
        st.sidebar.markdown('<div class="sidebar-logo">INTERVIEWER.<span style="color:#6366f1">AI</span></div>', unsafe_allow_html=True)
        
        if st.session_state.get('is_admin'):
            from modules.admin import render_admin_dashboard
            st.sidebar.markdown("### 👑 Admin Mode", unsafe_allow_html=True)
            if st.sidebar.button("Sign out", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.is_admin = False
                st.rerun()
            render_admin_dashboard()
            return
            
        round_names = [
            "📄 Resume Intel", "🧠 Neural Aptitude", 
            "💻 Technical Matrix", "⌨️ Holographic Coding", "🎙️ Vocal Pulse", "📊 Decision Desk", "🤖 Neural Assistant"
        ]
        
        for i, name in enumerate(round_names):
            active = st.session_state.current_round == i
            if st.sidebar.button(name, use_container_width=True, type="primary" if active else "secondary", key=f"nav_{i}"):
                st.session_state.current_round = i
                st.rerun()

        st.sidebar.markdown("<br><hr style='opacity: 0.1;'><br>", unsafe_allow_html=True)
        if st.sidebar.button("Sign out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

        # Core Sidebar Proctoring
        if not render_anticheat_panel(st.session_state.current_round):
            return

        # Round Rendering
        curr = st.session_state.current_round
        if curr == 0: render_round1()
        elif curr == 1: render_round2()
        elif curr == 2: render_round3()
        elif curr == 3: render_round4()
        elif curr == 4: render_round5()
        elif curr == 5: render_round7()
        elif curr == 6: render_round6()

if __name__ == "__main__":
    # Forced Hot-Reload Sentinel Comment V17 (Ensures submodules are fully re-imported)
    main()
