import streamlit as st
import asyncio
from playwright.async_api import async_playwright

st.title("🔎 Simple Playwright + Streamlit App (Async)")

async def fetch_title(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        title = await page.title()
        await browser.close()
        return title

url = st.text_input("Enter a URL:", "https://example.com")

if st.button("Fetch Title"):
    with st.spinner("Loading page..."):
        try:
            title = asyncio.run(fetch_title(url))
            st.success(f"Page title: **{title}**")
        except Exception as e:
            st.error(f"❌ Error: {e}")
