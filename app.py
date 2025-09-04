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
        # Detect environment (Render/Cloud vs Local)
        is_docker = os.environ.get("RENDER", None) is not None or os.environ.get("CI", None) is not None

        browser = await p.chromium.launch(
            headless=True if is_docker else True,  # Always headless in Docker/Render
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--disable-gpu",
                "--disable-software-rasterizer",
            ],
        )

        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        st.write("🔹 Opening IRCTC login page...")
        await page.goto(
            "https://www.irctc.co.in/nget/train-search",
            timeout=90000,
            wait_until="domcontentloaded",
        )

        # Close popup if it exists
        ads = await page.query_selector("//button[@class='btn btn-primary']")
        if ads:
            await ads.click()
            st.write("✅ Closed popup")

        # Click login button
        await page.click("xpath=//*[@class='search_btn loginText ng-star-inserted']")

        # Fill credentials
        await page.fill("input[placeholder='User Name']", username)
        await page.fill("input[placeholder='Password']", password)

        st.success("✅ Credentials entered successfully!")
        st.info("⚠️ Please enter captcha manually if required...")

        # Give some time before closing
        await asyncio.sleep(10)
        await browser.close()


if st.button("Login to IRCTC"):
    if not username or not password:
        st.error("❌ Please enter both username and password")
    else:
        try:
            asyncio.run(main(username, password))
        except Exception as e:
            st.error(f"❌ Error: {e}")
