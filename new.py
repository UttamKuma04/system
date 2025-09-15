import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64

# Streamlit UI
st.set_page_config(page_title="Selenium Web Screenshot", page_icon="🌐")
st.title("🌐 Selenium Web Scraper with Streamlit")

url = st.text_input("Enter a URL", "https://www.irctc.co.in/nget/train-search")
run_btn = st.button("Fetch Page")

if run_btn and url:
    try:
        # Selenium options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-http2")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(3)  # allow page to load

        title = driver.title
        st.success(f"✅ Page Title: {title}")

        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # Show screenshot in UI
        st.image(screenshot_path, caption=f"Screenshot of {url}", use_column_width=True)

        # Provide download button
        with open(screenshot_path, "rb") as file:
            btn = st.download_button(
                label="📥 Download Screenshot",
                data=file,
                file_name="screenshot.png",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")

