FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

RUN apt-get update && apt-get install -y xvfb

WORKDIR /app
COPY . .

CMD ["xvfb-run", "-a", "python", "app1.py"]
