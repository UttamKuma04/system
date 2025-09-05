import os, time
from playwright.sync_api import sync_playwright

PORT = os.getenv("PORT", "9222")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--remote-debugging-address=0.0.0.0",
            f"--remote-debugging-port={PORT}",
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )
    page = browser.new_page()
    page.goto("https://example.com")
    print("Loaded:", page.title())
    while True:
        time.sleep(10)
