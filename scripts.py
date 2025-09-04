import streamlit as st
from playwright.sync_api import sync_playwright

st.title("Playwright (Sync) URL Viewer")

url = st.text_input("Enter a URL", "https://www.python.org/")

if st.button("Open in Playwright"):
    st.write(f"Opening: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.goto(url, timeout=60000)
            screenshot_path = "screenshot.png"
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()
        st.success("Page opened successfully!")
        st.image(screenshot_path, caption=f"Screenshot of {url}")
    except Exception as e:
        st.error(f"Error: {e}")
