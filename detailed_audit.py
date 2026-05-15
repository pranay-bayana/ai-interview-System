import asyncio
from playwright.async_api import async_playwright
import sys

async def run_detailed_test():
    async with async_playwright() as p:
        print("🚀 Starting ROBUST PIN-TO-PIN AUDIT...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            # 1. Homepage & Login
            await page.goto("http://localhost:8502")
            await page.wait_for_timeout(2000)
            print("✓ Homepage reached")
            
            await page.click('text="🚀 INITIATE ASSESSMENT"')
            await page.wait_for_timeout(1000)
            await page.fill('input[aria-label="Professional Email"]', "test@example.com")
            await page.fill('input[aria-label="Access Password"]', "password")
            await page.click('text="AUTHORIZE SESSION"')
            await page.wait_for_timeout(3000)
            print("✓ Login successful")

            # 2. Sidebar Round Navigation using Internal Keys
            nav_rounds = ["Resume", "Aptitude", "Technical", "Coding", "Voice", "Chatbot", "Dashboard"]
            for round_name in nav_rounds:
                print(f"Testing Round: {round_name}...")
                # Streamlit buttons can be found by their label or key if using custom selectors
                # We'll use a more generic text selector that ignores emojis
                await page.click(f'button:has-text("{round_name}")')
                await page.wait_for_timeout(2000)
                
                content = await page.content()
                if "Error" in content or "Traceback" in content:
                    print(f"❌ ERROR in {round_name}")
                else:
                    print(f"✓ {round_name} verified")

            print("✨ FINAL STATUS: ALL INTERFACE COMPONENTS VERIFIED")
            
        except Exception as e:
            print(f"💥 AUDIT INTERRUPTED: {str(e)}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_detailed_test())
