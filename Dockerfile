FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chrome
RUN playwright install-deps
COPY . .
CMD ["pytest", "--alluredir=allure-results"]