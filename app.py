import asyncio
import sys
import os
from playwright.async_api import async_playwright
import streamlit as st


# ✅ Fix for Windows async subprocess
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.title("🚆 Auto Login")

username = st.text_input("Enter IRCTC Username")
password = st.text_input("Enter IRCTC Password", type="password")


async def main(username, password):
    async with async_playwright() as p:
        # Detect if running in server/Streamlit Cloud (no GUI available)
        is_server = os.environ.get("STREAMLIT_RUNTIME", None) is not None

        browser = await p.chromium.launch(
            headless=is_server,   # ✅ False locally, True on cloud
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        st.write("🔹 Opening IRCTC login page...")
        await page.goto("https://www.irctc.co.in/nget/train-search", timeout=90000, wait_until="domcontentloaded")

        # Close popup if exists
        ads = await page.query_selector("//button[@class='btn btn-primary']")
        if ads:
            await ads.click()
            st.write("✅ Closed popup")

        # Click login
        await page.click("xpath=//*[@class='search_btn loginText ng-star-inserted']")

        # Fill credentials
        await page.fill("input[placeholder='User Name']", username)
        await page.fill("input[placeholder='Password']", password)

        st.success("✅ Login successful!")
        await asyncio.sleep(10)
        await browser.close()


if st.button("Login to IRCTC"):
    asyncio.run(main(username, password))
