# System

Python browser automation experiments built with Streamlit, Selenium, and Playwright.

This repository contains small automation scripts for opening web pages, taking screenshots, fetching page titles, and testing IRCTC login-page automation flows. The Docker setup is focused on the Selenium Streamlit screenshot app in `new.py`.

## Project Structure

```text
system/
|-- app.py               # Streamlit IRCTC auto-login helper using Playwright
|-- demo.py              # Playwright demo that opens example.com and saves a screenshot
|-- new.py               # Streamlit Selenium app that captures and downloads screenshots
|-- test.py              # Synchronous Playwright script for IRCTC page title and screenshot
|-- test_playwright.py   # Streamlit Playwright app that fetches a URL title
|-- requirements.txt     # Python dependencies currently used by the Selenium app
|-- Dockerfile           # Container image for running new.py with Streamlit
`-- README.md            # Project documentation
```

## What It Does

### `app.py`

Runs a Streamlit interface for IRCTC login automation. It asks for an IRCTC username and password, opens the IRCTC train-search page with Playwright, closes the popup when present, opens the login dialog, fills the credentials, and shows screenshots of each major step.

Captcha handling is not automated. The app displays a message asking the user to complete captcha manually when required.

### `new.py`

Runs a Streamlit app backed by Selenium. The user enters a URL, the app launches headless Chrome, loads the page, displays the page title, saves a screenshot as `screenshot.png`, displays it in the UI, and provides a download button.

The Dockerfile is configured to run this file.

### `test_playwright.py`

Runs a Streamlit page-title fetcher using Playwright. The user enters a URL, the script opens it in Chromium, saves a screenshot, reads the page title, and shows the title in Streamlit.

### `test.py`

Runs a simple synchronous Playwright script against the IRCTC train-search page. It opens Chromium, prints the page title, saves `screenshot.png`, waits briefly, and closes the browser.

### `demo.py`

Runs a Playwright demo against `https://example.com`, saves a screenshot, and closes the browser. On Linux, it uses `pyvirtualdisplay` to provide a virtual display for non-headless browser execution.

## Tech Stack

- Python
- Streamlit
- Selenium
- Playwright
- Chrome or Chromium
- Docker

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source venv/bin/activate
```

Install the dependencies listed in the project:

```bash
pip install -r requirements.txt
```

For scripts that use Playwright, install Playwright and its Chromium browser:

```bash
pip install playwright
python -m playwright install chromium
```

For `demo.py` on Linux, install the optional virtual display dependency:

```bash
pip install pyvirtualdisplay
```

## Running the Apps

Run the Selenium screenshot Streamlit app:

```bash
streamlit run new.py
```

Run the IRCTC Playwright Streamlit app:

```bash
streamlit run app.py
```

Run the Playwright page-title Streamlit app:

```bash
streamlit run test_playwright.py
```

Run the standalone Playwright scripts:

```bash
python test.py
python demo.py
```

## Docker Usage

Build the Docker image:

```bash
docker build -t system-streamlit .
```

Run the container:

```bash
docker run -p 8501:8501 system-streamlit
```

Open the Streamlit app at:

```text
http://localhost:8501
```

The container runs `new.py` by default.

## Runtime Notes

- `app.py` and `test_playwright.py` require Playwright, which is not listed in the current `requirements.txt`.
- `new.py` requires Chrome or Chromium support for Selenium. The Dockerfile installs Google Chrome and Chromium Driver.
- Several scripts write `screenshot.png` in the project directory.
- Some scripts launch browsers with `headless=False`, so they require a desktop session or virtual display.
- IRCTC pages can change selectors or block automation, so those scripts may need selector updates over time.

## Security Notes

- Do not commit real IRCTC credentials or other secrets.
- The Streamlit apps accept credentials or URLs from the user at runtime.
- Captcha solving is intentionally left to the user.

## Suggested Improvements

- Move Playwright dependencies into `requirements.txt` if all scripts should run from one install command.
- Split standalone scripts and Streamlit apps into separate directories.
- Add automated tests for helper logic.
- Avoid writing every screenshot to the same `screenshot.png` path when running multiple scripts.
- Add environment-specific configuration for browser headless mode.
