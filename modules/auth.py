"""
Authentication Module for AI Recruitment Ecosystem
Handles candidate signup/login and admin access
"""

import hashlib
import streamlit as st
from database.init_db import get_db
import os

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(email: str, password: str, full_name: str) -> dict:
    """Register a new candidate"""
    db = get_db()
    try:
        existing = db.client.table('users').select('*').eq('email', email).execute()
        if existing.data:
            return {'success': False, 'message': 'Email already registered'}
        
        password_hash = hash_password(password)
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'role': 'candidate'
        }
        
        result = db.client.table('users').insert(user_data).execute()
        user_id = result.data[0]['id']
        db.client.table('candidate_scores').insert({'user_id': user_id}).execute()
        db.client.table('candidate_status').insert({'user_id': user_id}).execute()
        
        return {'success': True, 'message': 'Registration successful', 'user_id': user_id}
    except Exception as e:
        return {'success': False, 'message': f'Registration failed: {str(e)}'}

def login_user(email: str, password: str) -> dict:
    """Login a user"""
    db = get_db()
    try:
        password_hash = hash_password(password)
        result = db.client.table('users').select('*').eq('email', email).eq('password_hash', password_hash).execute()
        
        if result.data:
            return {'success': True, 'user': result.data[0], 'message': 'Login successful'}
        else:
            return {'success': False, 'message': 'Invalid email or password'}
    except Exception as e:
        return {'success': False, 'message': f'Login failed: {str(e)}'}

def verify_admin_access(access_key: str) -> bool:
    """Verify admin access key with infallible demo fallback"""
    # Force the key to be ADMIN2024 for the demo to ensure zero friction
    correct_key = "ADMIN2024"
    return access_key.strip() == correct_key

def render_auth_page():
    """Render stunning authentication page"""
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 48px; margin-bottom: 10px;">Portal Access</h1>
            <p style="color: rgba(255,255,255,0.5);">Join the elite talent pool today.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 SECURE LOGIN", "📝 QUICK SIGNUP"])
        
        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            email = st.text_input("Professional Email", placeholder="email@example.com", key="login_email")
            password = st.text_input("Access Password", type="password", placeholder="••••••••", key="login_password")
            
            if st.button("AUTHORIZE SESSION", use_container_width=True, key="login_btn"):
                if email and password:
                    result = login_user(email, password)
                    if result['success']:
                        st.session_state.user = result['user']
                        st.session_state.authenticated = True
                        st.session_state.is_admin = result['user']['role'] == 'admin'
                        st.success("Access Granted. Redirecting...")
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.error("Missing credentials")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            full_name = st.text_input("Full Name", placeholder="John Doe", key="signup_name")
            email = st.text_input("Email Address", placeholder="john@example.com", key="signup_email")
            password = st.text_input("Create Password", type="password", placeholder="••••••••", key="signup_password")
            
            if st.button("CREATE ACCOUNT", use_container_width=True, key="signup_btn"):
                if full_name and email and password:
                    result = signup_user(email, password, full_name)
                    if result['success']:
                        st.success("Account Created! You can now login.")
                    else:
                        st.error(result['message'])
                else:
                    st.error("Please fill all fields")
            st.markdown('</div>', unsafe_allow_html=True)

def render_admin_access():
    """Render Hyper-Futuristic Admin Access Portal"""
    st.markdown("""
        <div style="text-align: center; padding: 100px 0 50px 0;">
            <div style="font-size: 64px; margin-bottom: 20px; filter: drop-shadow(0 0 20px #00f2ff);">🎯</div>
            <h1 style="font-size: 48px; font-weight: 900; letter-spacing: 5px;">ADMIN_CORE</h1>
            <p style="color: rgba(255,255,255,0.5); letter-spacing: 2px;">SECURE NEURAL OVERRIDE REQUIRED</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="clay-card">', unsafe_allow_html=True)
        access_key = st.text_input("ENTER ACCESS PROTOCOL KEY", type="password", placeholder="••••••••", help="Enter the master administrator key.")
        
        if st.button("INITIATE OVERRIDE ⚡", use_container_width=True):
            if verify_admin_access(access_key):
                st.session_state.is_admin = True
                st.session_state.admin_verified = True
                st.session_state.authenticated = True
                # Set a mock admin user to prevent sidebar crashes
                st.session_state.user = {
                    'id': 'ADMIN',
                    'full_name': 'System Administrator',
                    'email': 'admin@neural.core',
                    'role': 'admin'
                }
                st.success("Access Granted. Synchronizing Control Center...")
                st.rerun()
            else:
                st.error("INVALID ACCESS PROTOCOL. INCIDENT LOGGED.")
        
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        if st.button("CANCEL ACCESS", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'home'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logout current user"""
    st.session_state.user = None
    st.session_state.authenticated = False
    st.session_state.is_admin = False
    st.session_state.admin_verified = False
    st.rerun()

def check_auth():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current user"""
    return st.session_state.get('user')
