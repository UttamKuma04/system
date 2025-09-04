import asyncio
import base64
from io import BytesIO
from PIL import Image
from playwright.async_api import async_playwright
import streamlit as st


# Launch browser safely
async def launch_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,  # set True if running on server
        args=["--no-sandbox", "--disable-setuid-sandbox",  "--start-maximized",]
    )
    context = await browser.new_context()
    page = await context.new_page()
    return playwright, browser, page


async def open_login(username, password, captcha_input=None):
    playwright, browser, page = await launch_browser()

    try:
        st.write("🔹 Opening IRCTC login page...")
        await page.goto(
            "https://www.irctc.co.in/nget/train-search",
            timeout=90000,
            wait_until="domcontentloaded"
        )

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
                st.image(img, caption="🔐 Captcha")

            # Wait for user input
            if not captcha_input:
                st.warning("⚠️ Please enter captcha above and click 'Submit Login'")
                return  # stop here, keep browser open

            # Fill captcha
            await page.fill("input[placeholder='Enter Captcha']", captcha_input)
            st.write(f"🧩 Captcha entered: `{captcha_input}`")

            # Submit login
            await page.click(
                "xpath=//button[@class ='search_btn train_Search train_Search_custom_hover']"
            )
            st.success("✅ Login attempted!")

            try:
                await page.wait_for_selector("xpath=//a[contains(text(),'Logout')]", timeout=15000)
                st.success("🎉 Logged in successfully!")
            except:
                st.warning("⚠️ Login may have failed. Please check credentials/captcha.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        await browser.close()
        await playwright.stop()


# -------- Streamlit UI --------
st.title("🚆 IRCTC Auto Login")

username = st.text_input("IRCTC Username")
password = st.text_input("IRCTC Password", type="password")
captcha_input = st.text_input("Enter Captcha (after image shown)")

if st.button("Start Login"):
    if username and password:
        asyncio.run(open_login(username, password, captcha_input))
    else:
        st.warning("⚠️ Please enter both username and password")
