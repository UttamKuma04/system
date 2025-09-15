from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.irctc.co.in/nget/train-search")
    print("Page Title:", page.title())
    page.screenshot(path="screenshot.png")

    time.sleep(20)
    browser.close()
