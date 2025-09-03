import asyncio
import sys
from playwright.async_api import async_playwright
import streamlit as st
import re


# ✅ Fix for Windows async subprocess
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.title("🚆Auto Login")

username = st.text_input("Enter IRCTC Username")
password = st.text_input("Enter IRCTC Password", type="password")


async def main(username, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
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

        # Handle captcha
        # captcha_element = await page.wait_for_selector("//img[@class='captcha-img']")
        # base64_string = await captcha_element.get_attribute("src")

        # if base64_string:
        #     base64_string = base64_string.split(",")[1]
        #     img_data = base64.b64decode(base64_string)

        #     with BytesIO(img_data) as buffer:
        #         img = Image.open(buffer).convert("RGB")
        #         img.save("captcha.jpg")

        #     raw_text = tess.image_to_string(Image.open("captcha.jpg"))
        #     captcha_input = re.sub(r"[^A-Za-z0-9]", "", raw_text).strip()

        #     await page.fill("input[placeholder='Enter Captcha']", captcha_input)
        #     st.write(f"🧩 Captcha entered: `{captcha_input}`")

        # # Submit login
        # await page.click("xpath=//button[@class ='search_btn train_Search train_Search_custom_hover']")

        st.success("✅ Login successful!")
        await asyncio.sleep(10)
        await browser.close()


if st.button("Login to IRCTC"):
    asyncio.run(main(username, password))
