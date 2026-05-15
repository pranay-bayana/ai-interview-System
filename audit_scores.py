import asyncio
from playwright.async_api import async_playwright

async def audit_scores():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8502")
        await page.wait_for_timeout(2000)
        
        # Login
        await page.click('text="🚀 INITIATE ASSESSMENT"')
        await page.fill('input[aria-label="Professional Email"]', "test@example.com")
        await page.fill('input[aria-label="Access Password"]', "password")
        await page.click('text="AUTHORIZE SESSION"')
        await page.wait_for_timeout(3000)
        
        # Go to Aptitude
        await page.click('button:has-text("Aptitude")')
        await page.wait_for_timeout(2000)
        
        # Select answers
        for i in range(1, 6):
            # Click the 'c' option for each (some will be right)
            await page.click(f'label:has-text("C.")')
            if i < 5:
                await page.click('text="NEXT ➡️"')
                await page.wait_for_timeout(500)
        
        # Submit
        await page.click('text="SUBMIT PROFILE 🎯"')
        await page.wait_for_timeout(3000)
        
        # Check if score is visible
        content = await page.content()
        if "/05" in content:
            print(f"✓ APTITUDE SCORE VISIBLE: {content[content.find('/05')-1:content.find('/05')+3]}")
        else:
            print("❌ SCORE NOT VISIBLE AFTER SUBMISSION")
            
        # Go to Dashboard
        await page.click('button:has-text("Dashboard")')
        await page.wait_for_timeout(3000)
        content = await page.content()
        if "SCORE:" in content:
            print("✓ DASHBOARD SCORE VISIBLE")
        else:
            print("❌ DASHBOARD SCORE NOT VISIBLE")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit_scores())
