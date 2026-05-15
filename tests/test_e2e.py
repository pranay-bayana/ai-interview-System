"""
Playwright E2E Tests for AI Recruitment Ecosystem
Tests all buttons, sliders, and form submissions
"""

from playwright.sync_api import Page, expect
import pytest

# Test configuration
BASE_URL = "http://localhost:8501"

def test_homepage_loads(page: Page):
    """Test that the homepage loads correctly"""
    page.goto(BASE_URL)
    expect(page).to_have_title("AI Recruitment Ecosystem")
    expect(page.locator("h1")).to_contain_text("AI Recruitment Ecosystem")

def test_signup_flow(page: Page):
    """Test user signup flow"""
    page.goto(BASE_URL)
    
    # Click on Sign Up tab
    page.click("text=Sign Up")
    
    # Fill in signup form
    page.fill('input[placeholder="Enter your full name"]', "Test User")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Create a password"]', "password123")
    page.fill('input[placeholder="Confirm your password"]', "password123")
    
    # Click signup button
    page.click('button:has-text("Sign Up")')
    
    # Verify success message
    expect(page.locator("text=Registration successful")).to_be_visible()

def test_login_flow(page: Page):
    """Test user login flow"""
    page.goto(BASE_URL)
    
    # Click on Login tab
    page.click("text=Login")
    
    # Fill in login form
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    
    # Click login button
    page.click('button:has-text("Login")')
    
    # Verify login success
    expect(page.locator("text=Login successful")).to_be_visible()

def test_round1_resume_upload(page: Page):
    """Test Round 1: Resume Upload"""
    page.goto(BASE_URL)
    
    # Login first
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 1
    page.click('button:has-text("Resume")')
    
    # Verify round title
    expect(page.locator("text=Round 1: Resume Upload")).to_be_visible()

def test_round2_aptitude(page: Page):
    """Test Round 2: Aptitude Assessment"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 2
    page.click('button:has-text("Aptitude")')
    
    # Verify round title
    expect(page.locator("text=Round 2: Aptitude Assessment")).to_be_visible()
    
    # Verify timer display
    expect(page.locator("text=10:00")).to_be_visible()

def test_round3_technical(page: Page):
    """Test Round 3: Technical Questions"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 3
    page.click('button:has-text("Technical")')
    
    # Verify round title
    expect(page.locator("text=Round 3: Technical Questions")).to_be_visible()
    
    # Verify role selector
    expect(page.locator("select")).to_be_visible()

def test_round4_coding(page: Page):
    """Test Round 4: Coding Challenge"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 4
    page.click('button:has-text("Coding")')
    
    # Verify round title
    expect(page.locator("text=Round 4: Coding Challenge")).to_be_visible()
    
    # Verify language selector
    expect(page.locator("select")).to_be_visible()

def test_round5_voice(page: Page):
    """Test Round 5: HR Voice Interview"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 5
    page.click('button:has-text("HR Voice")')
    
    # Verify round title
    expect(page.locator("text=Round 5: HR Voice Interview")).to_be_visible()

def test_round6_chatbot(page: Page):
    """Test Round 6: AI Chatbot"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 6
    page.click('button:has-text("Chatbot")')
    
    # Verify round title
    expect(page.locator("text=Round 6: AI Interview Assistant")).to_be_visible()
    
    # Verify chat input
    expect(page.locator('input[placeholder*="Type your question"]')).to_be_visible()

def test_round7_dashboard(page: Page):
    """Test Round 7: Performance Dashboard"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 7
    page.click('button:has-text("Dashboard")')
    
    # Verify round title
    expect(page.locator("text=Round 7: Performance Dashboard")).to_be_visible()

def test_admin_access(page: Page):
    """Test Admin Access verification"""
    page.goto(BASE_URL)
    
    # Click Admin Access
    page.click('button:has-text("Admin Access")')
    
    # Verify access key input
    expect(page.locator('input[type="password"]')).to_be_visible()
    
    # Enter access key
    page.fill('input[type="password"]', "ADMIN2024")
    
    # Click verify
    page.click('button:has-text("Verify Access")')
    
    # Verify admin dashboard loads
    expect(page.locator("text=Admin Decision Desk")).to_be_visible()

def test_logout(page: Page):
    """Test logout functionality"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Click logout
    page.click('button:has-text("Logout")')
    
    # Verify logout success
    expect(page.locator("text=Logged out successfully")).to_be_visible()

def test_form_validation(page: Page):
    """Test form validation"""
    page.goto(BASE_URL)
    
    # Try to submit empty form
    page.click("text=Sign Up")
    page.click('button:has-text("Sign Up")')
    
    # Verify error message
    expect(page.locator("text=Please fill in all fields")).to_be_visible()

def test_password_mismatch(page: Page):
    """Test password mismatch validation"""
    page.goto(BASE_URL)
    
    # Click Sign Up
    page.click("text=Sign Up")
    
    # Fill with mismatched passwords
    page.fill('input[placeholder="Enter your full name"]', "Test User")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Create a password"]', "password123")
    page.fill('input[placeholder="Confirm your password"]', "different123")
    
    # Click signup
    page.click('button:has-text("Sign Up")')
    
    # Verify error
    expect(page.locator("text=Passwords do not match")).to_be_visible()

def test_slider_interaction(page: Page):
    """Test slider interaction in Round 5"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 5
    page.click('button:has-text("HR Voice")')
    
    # Verify slider exists
    expect(page.locator('input[type="range"]')).to_be_visible()

def test_textarea_interaction(page: Page):
    """Test textarea interaction in Round 3"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 3
    page.click('button:has-text("Technical")')
    
    # Verify textarea exists
    expect(page.locator('textarea')).to_be_visible()

def test_selectbox_interaction(page: Page):
    """Test selectbox interaction in Round 3 and 4"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 3
    page.click('button:has-text("Technical")')
    
    # Verify selectbox exists
    expect(page.locator('select')).to_be_visible()

def test_navigation_between_rounds(page: Page):
    """Test navigation between different rounds"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate through rounds
    page.click('button:has-text("Resume")')
    expect(page.locator("text=Round 1: Resume Upload")).to_be_visible()
    
    page.click('button:has-text("Aptitude")')
    expect(page.locator("text=Round 2: Aptitude Assessment")).to_be_visible()
    
    page.click('button:has-text("Technical")')
    expect(page.locator("text=Round 3: Technical Questions")).to_be_visible()

def test_responsive_design(page: Page):
    """Test responsive design on mobile viewport"""
    page.goto(BASE_URL)
    page.set_viewport_size({"width": 375, "height": 667})
    
    # Verify elements are still visible
    expect(page.locator("h1")).to_be_visible()
    expect(page.locator("button")).to_be_visible()

def test_anticheat_round1_face_detection(page: Page):
    """Test face detection in Round 1 (resume upload)"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 1
    page.click('button:has-text("Resume")')
    
    # Verify face detection is active
    expect(page.locator("text=Face Detection Active")).to_be_visible()
    expect(page.locator("text=Enable Camera for Face Detection")).to_be_visible()

def test_anticheat_round2_tab_switching_blocked(page: Page):
    """Test tab switching is blocked in Round 2"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 2
    page.click('button:has-text("Aptitude")')
    
    # Verify tab switching warning is displayed
    expect(page.locator("text=Tab Switching Blocked")).to_be_visible()
    expect(page.locator("text=Switching tabs or windows during this round is prohibited")).to_be_visible()

def test_anticheat_round3_fullscreen_required(page: Page):
    """Test fullscreen requirement in Round 3"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has_text("Login")')
    
    # Navigate to Round 3
    page.click('button:has-text("Technical")')
    
    # Verify fullscreen requirement is displayed
    expect(page.locator("text=Fullscreen Required")).to_be_visible()

def test_anticheat_round4_strict_mode(page: Page):
    """Test strict anti-cheating mode in Round 4 (coding)"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 4
    page.click('button:has-text("Coding")')
    
    # Verify all anti-cheating measures are active
    expect(page.locator("text=Face Detection Active")).to_be_visible()
    expect(page.locator("text=Tab Switching Blocked")).to_be_visible()
    expect(page.locator("text=Fullscreen Required")).to_be_visible()

def test_anticheat_round5_strict_mode(page: Page):
    """Test strict anti-cheating mode in Round 5 (voice interview)"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 5
    page.click('button:has-text("HR Voice")')
    
    # Verify all anti-cheating measures are active
    expect(page.locator("text=Face Detection Active")).to_be_visible()
    expect(page.locator("text=Tab Switching Blocked")).to_be_visible()
    expect(page.locator("text=Fullscreen Required")).to_be_visible()

def test_anticheat_round6_relaxed_mode(page: Page):
    """Test relaxed anti-cheating mode in Round 6 (chatbot)"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 6
    page.click('button:has-text("Chatbot")')
    
    # Verify anti-cheating measures are NOT active (relaxed mode)
    expect(page.locator("text=Face Detection Active")).not_to_be_visible()
    expect(page.locator("text=Tab Switching Blocked")).not_to_be_visible()
    expect(page.locator("text=Fullscreen Required")).not_to_be_visible()

def test_anticheat_round7_relaxed_mode(page: Page):
    """Test relaxed anti-cheating mode in Round 7 (dashboard)"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 7
    page.click('button:has-text("Dashboard")')
    
    # Verify anti-cheating measures are NOT active (relaxed mode)
    expect(page.locator("text=Face Detection Active")).not_to_be_visible()
    expect(page.locator("text=Tab Switching Blocked")).not_to_be_visible()
    expect(page.locator("text=Fullscreen Required")).not_to_be_visible()

def test_anticheat_violation_message(page: Page):
    """Test anti-cheating violation message display"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to a strict round
    page.click('button:has-text("Aptitude")')
    
    # Verify violation warning text is present
    expect(page.locator("text=You have 3 warnings before disqualification")).to_be_visible()

def test_camera_input_component(page: Page):
    """Test camera input component for face detection"""
    page.goto(BASE_URL)
    
    # Login
    page.click("text=Login")
    page.fill('input[placeholder="Enter your email"]', "test@example.com")
    page.fill('input[placeholder="Enter your password"]', "password123")
    page.click('button:has-text("Login")')
    
    # Navigate to Round 1
    page.click('button:has-text("Resume")')
    
    # Verify camera input exists
    expect(page.locator('input[type="file"][accept*="image"]')).to_be_visible()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
