FROM python:3.10-slim

# Install system dependencies for Chromium + Xvfb
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip fonts-liberation libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 \
    libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-6 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libxshmfence1 libxss1 libxtst6 xdg-utils xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium
RUN playwright install --with-deps chromium

# Copy all files
COPY . .

# Streamlit config (safety)
RUN mkdir -p .streamlit && echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
address = \"0.0.0.0\"\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > .streamlit/config.toml

# Expose port (optional for docs, Render uses $PORT anyway)
EXPOSE 10000

# ✅ Use bash -c so $PORT expands correctly at runtime
CMD bash -c "xvfb-run -a streamlit run test_playwright.py --server.port=\$PORT --server.address=0.0.0.0"
