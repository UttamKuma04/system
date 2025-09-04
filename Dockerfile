FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive

# Install system deps for Chromium + xvfb
RUN apt-get update -q && \
    apt-get install -y -qq --no-install-recommends \
        wget \
        curl \
        unzip \
        xauth \
        xvfb \
        fonts-liberation \
        libasound2 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnss3 \
        libnspr4 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxkbcommon0 \
        libxrandr2 \
        xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps + Playwright Chromium
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install playwright && \
    playwright install --with-deps chromium

# Copy app
COPY app.py .

# Prevent Streamlit from asking for email
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose Render port
EXPOSE 10000

# Run Streamlit on Render's $PORT
CMD xvfb-run -s "-screen 0 1280x900x24" streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
