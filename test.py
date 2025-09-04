# import sys
# import asyncio
# from playwright.async_api import async_playwright
# import streamlit as st

# # ✅ Fix for Windows event loop
# if sys.platform.startswith("win"):
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# st.set_page_config(page_title="URL Title Fetcher", page_icon="🌐")
# st.title("🌐 Get Page Title with Playwright")

# url = st.text_input("Enter a URL", "https://example.com")

# async def get_title(target_url: str):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=False,
#             args=[
#                 "--no-sandbox",
#                 "--disable-dev-shm-usage",
#                 "--disable-http2",                  # ✅ Fix ERR_HTTP2_PROTOCOL_ERROR
#                 "--ignore-certificate-errors",
#                 "--disable-blink-features=AutomationControlled",
#                 "--disable-features=IsolateOrigins,site-per-process",
#                 "--enable-features=NetworkService,NetworkServiceInProcess"
#             ]
#         )
#         page = await browser.new_page()
#         await page.goto(target_url, timeout=120000, wait_until="domcontentloaded")
#         title = await page.title()
#         await browser.close()
#         return title

# if st.button("Fetch Title"):
#     if url:
#         try:
#             title = asyncio.run(get_title(url))
#             st.success(f"✅ Page title: {title}")
#         except Exception as e:
#             st.error(f"❌ Error fetching title: {e}")
#     else:
#         st.warning("⚠️ Please enter a valid URL")


import sys
import asyncio
from playwright.async_api import async_playwright
import streamlit as st

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="URL Title Fetcher", page_icon="🌐")
st.title("🌐 Get Page Title with Playwright (Remote Chrome)")

url = st.text_input("Enter a URL", "https://example.com")
chrome_ws = st.text_input("Enter Chrome WebSocket URL", "ws://127.0.0.1:9222")

async def get_title(target_url: str, ws_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0] if browser.contexts else await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        page = await context.new_page()
        await page.goto(target_url, timeout=120000, wait_until="networkidle")
        title = await page.title()
        await browser.close()
        return title

if st.button("Fetch Title"):
    if url and chrome_ws:
        try:
            title = asyncio.run(get_title(url, chrome_ws))
            st.success(f"✅ Page title: {title}")
        except Exception as e:
            st.error(f"❌ Error fetching title: {e}")
    else:
        st.warning("⚠️ Please enter both URL and Chrome WebSocket endpoint")
