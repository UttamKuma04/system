import sys
import asyncio
from playwright.async_api import async_playwright
import streamlit as st

# ✅ Fix for Windows event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="URL Title Fetcher", page_icon="🌐")
st.title("🌐 Get Page Title with Playwright")

url = st.text_input("Enter a URL", "https://example.com")

async def get_title(target_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-http2",                  # ✅ Fix ERR_HTTP2_PROTOCOL_ERROR
                "--ignore-certificate-errors",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--enable-features=NetworkService,NetworkServiceInProcess"
            ]
        )
        page = await browser.new_page()
        await page.goto(target_url, timeout=120000, wait_until="domcontentloaded")
        title = await page.title()
        await browser.close()
        return title

if st.button("Fetch Title"):
    if url:
        try:
            title = asyncio.run(get_title(url))
            st.success(f"✅ Page title: {title}")
        except Exception as e:
            st.error(f"❌ Error fetching title: {e}")
    else:
        st.warning("⚠️ Please enter a valid URL")

