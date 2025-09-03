import asyncio
import sys
import base64
from PIL import Image
from io import BytesIO
from playwright.async_api import async_playwright
import streamlit as st

# ✅ Fix for Windows async subprocess
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.title("🚆 Auto Login")

username = st.text_input("Enter IRCTC Username")
password = st.text_input("Enter IRCTC Password", type="password")

# Keep browser context alive across reruns
if "page" not in st.session_state:
    st.session_state.page = None
if "browser" not in st.session_state:
    st.session_state.browser = None


async def launch_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
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
        return browser, page


async def open_login(username, password):
    browser, page = await launch_browser()

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

    # Handle captcha
    captcha_element = await page.wait_for_selector("//img[@class='captcha-img']")
    base64_string = await captcha_element.get_attribute("src")

    if base64_string:
        base64_string = base64_string.split(",")[1]
        img_data = base64.b64decode(base64_string)

        with BytesIO(img_data) as buffer:
            img = Image.open(buffer).convert("RGB")

        # Show captcha image in Streamlit
        st.image(img, caption="🔒 Captcha", use_container_width=False)

    # Save page/browser in session state for next step
    st.session_state.page = page
    st.session_state.browser = browser


async def submit_captcha(captcha_input):
    page = st.session_state.page
    browser = st.session_state.browser

    if not page or not browser:
        st.error("❌ Please start login first!")
        return

    await page.fill("input[placeholder='Enter Captcha']", captcha_input)
    st.write(f"🧩 Captcha entered: `{captcha_input}`")

    # Submit login
    await page.click("xpath=//button[@class ='search_btn train_Search train_Search_custom_hover']")
    st.success("✅ Login successful!")

    await asyncio.sleep(10)
    await browser.close()
    st.session_state.page = None
    st.session_state.browser = None


# --- Streamlit buttons ---
if st.button("🔐 Start Login"):
    asyncio.run(open_login(username, password))

captcha_input = st.text_input("Enter Captcha")
if st.button("🚀 Submit Captcha"):
    asyncio.run(submit_captcha(captcha_input))
