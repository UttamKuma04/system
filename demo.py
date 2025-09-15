import sys
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch Chromium with GUI mode (headless=False)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://example.com")
        await page.screenshot(path="screenshot.png")
        print("✅ Screenshot saved as screenshot.png")

        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    # On Linux server, wrap inside Xvfb
    if sys.platform.startswith("linux"):
        from pyvirtualdisplay import Display
        with Display(visible=0, size=(1920, 1080)):
            asyncio.run(run())
    else:
        asyncio.run(run())
