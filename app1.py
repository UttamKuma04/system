from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,  # 👈 headed mode works now
        args=[
            "--remote-debugging-address=0.0.0.0",
            "--remote-debugging-port=9222",
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )
    page = browser.new_page()
    page.goto("https://example.com")
    print("Loaded:", page.title())
    while True:
        time.sleep(10)
