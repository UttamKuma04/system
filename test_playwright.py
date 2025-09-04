import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.goto("https://example.com", timeout=60000)
        print("✅ Page title:", await page.title())
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
