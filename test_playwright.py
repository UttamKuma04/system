import sys
import asyncio
from playwright.async_api import async_playwright
import streamlit as st

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="URL Title Fetcher", page_icon="🌐")
st.title("🌐 Get Page Title")

url = st.text_input("Enter a URL", "https://example.com")

async def get_title(target_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-dev-shm-usage",
                   "--remote-debugging-port=9222",
                   "--disable-http2",
                   ]
        )
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # page = await browser.new_page()
        page = await context.new_page()
        await page.goto(target_url, timeout=60000)
        await page.screenshot(path="screenshot.png")
        title = await page.title()
        await browser.close()
        return title

if st.button("Fetch Title"):
    if url:
        try:
            title = asyncio.run(get_title(url))
            st.success(f"✅ Page title: {title}")
        except Exception as e:
            st.error(f"Error fetching title: {e}")
    else:
        st.warning("Please enter a valid URL")