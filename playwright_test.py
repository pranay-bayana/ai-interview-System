import asyncio
from playwright.async_api import async_playwright
import os

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "http://localhost:8502"
        print(f"Navigating to {url}...")
        await page.goto(url)
        await page.wait_for_timeout(3000)
        await page.screenshot(path="homepage.png")
        print("✓ Homepage captured")
        
        # Click Initiate Assessment
        await page.click('text="🚀 INITIATE ASSESSMENT"')
        await page.wait_for_timeout(2000)
        await page.screenshot(path="auth_page.png")
        print("✓ Auth page captured")
        
        # Login
        await page.fill('input[aria-label="Professional Email"]', "test@example.com")
        await page.fill('input[aria-label="Access Password"]', "password")
        await page.click('text="AUTHORIZE SESSION"')
        await page.wait_for_timeout(3000)
        await page.screenshot(path="after_login.png")
        print("✓ Login successful")
        
        # Navigate through rounds
        rounds = ["Resume", "Aptitude", "Technical", "Coding", "Voice", "Chatbot", "Dashboard"]
        for r in rounds:
            print(f"Testing Round: {r}...")
            # Sidebar buttons have icon + text
            selector = f'button:has-text("{r}")'
            await page.click(selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"round_{r.lower()}.png")
            print(f"✓ Round {r} verified")
            
        # Logout
        print("Logging out...")
        await page.click('text="🚪 Logout Session"')
        await page.wait_for_timeout(2000)
        await page.screenshot(path="final_logout.png")
        print("✓ Logout successful")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_test())
