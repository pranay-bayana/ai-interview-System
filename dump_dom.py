import asyncio
from playwright.async_api import async_playwright

async def dump_dom():
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
        
        # Dump buttons
        buttons = await page.query_selector_all('button')
        print(f"Found {len(buttons)} buttons:")
        for btn in buttons:
            text = await btn.inner_text()
            print(f"- '{text}'")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump_dom())
