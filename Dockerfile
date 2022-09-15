FROM python:3.8

COPY . /app

RUN apt update

RUN apt install ffmpeg -y
RUN pip install youtube_dl azure-storage-blob PyYAML pytz

WORKDIR /app

CMD [ "python", "main.py"]