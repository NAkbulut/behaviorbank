FROM python:3.8

COPY . /app

RUN apt update

RUN pip install azure-storage-blob azure-cosmos PyYAML pytz selenium webdriver-manager

WORKDIR /app

CMD ["python", "bb-web-scraper.py"]