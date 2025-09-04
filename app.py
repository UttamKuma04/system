import asyncio
import sys
import os
from playwright.async_api import async_playwright
import streamlit as st

# ✅ Fix for Windows async subprocess handling
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="IRCTC Auto Login", page_icon="🚆")
st.title("🚆 IRCTC Auto Login")

username = st.text_input("Enter IRCTC Username")
password = st.text_input("Enter IRCTC Password", type="password")


async def main(username: str, password: str):
    async with async_playwright() as p:
        # Detect if running in Render/Docker
        is_docker = os.environ.get("RENDER", None) is not None or os.environ.get("CI", None) is not None

        # ✅ Launch Chromium with safe flags
        browser = await p.chromium.launch(
            headless=False,  # Always headless on server
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-http2",  # ✅ Fix IRCTC HTTP2 issue
                "--ignore-certificate-errors",
                "--disable-features=IsolateOrigins,site-per-process",
                "--enable-features=NetworkService,NetworkServiceInProcess",
            ],
        )

        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        st.write("🔹 Opening IRCTC login page...")
        try:
            await page.goto(
                "https://www.irctc.co.in/nget/train-search",
                timeout=120000,
                wait_until="networkidle",  # ✅ wait for network settle
            )
        except Exception as e:
            st.error(f"❌ Failed to load IRCTC: {e}")
            await browser.close()
            return

        # Close popup if exists
        try:
            ads = await page.query_selector("//button[@class='btn btn-primary']")
            if ads:
                await ads.click()
                st.write("✅ Closed popup")
        except Exception:
            st.write("ℹ️ No popup found")

        # Click login button
        try:
            await page.click("xpath=//*[@class='search_btn loginText ng-star-inserted']")
        except Exception as e:
            st.error(f"❌ Could not click login button: {e}")
            await browser.close()
            return

        # Fill credentials
        try:
            await page.fill("input[placeholder='User Name']", username)
            await page.fill("input[placeholder='Password']", password)
            st.success("✅ Credentials entered successfully!")
            st.info("⚠️ Please enter captcha manually if required...")
        except Exception as e:
            st.error(f"❌ Error filling credentials: {e}")

        # Give some time before closing
        await asyncio.sleep(10)
        await browser.close()


# Button handler
if st.button("Login to IRCTC"):
    if not username or not password:
        st.error("❌ Please enter both username and password")
    else:
        try:
            asyncio.run(main(username, password))
        except Exception as e:
            st.error(f"❌ Error: {e}")
