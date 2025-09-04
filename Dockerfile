FROM python:3.13-slim

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip fonts-liberation libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 \
    libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-6 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libxshmfence1 libxss1 libxtst6 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium with dependencies
RUN playwright install --with-deps chromium

COPY . .

# ✅ Run Streamlit instead of Python script
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
