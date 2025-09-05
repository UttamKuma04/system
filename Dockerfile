FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

WORKDIR /app
COPY . .

EXPOSE 9222

CMD ["python", "app1.py"]
