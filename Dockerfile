FROM python:3.12-slim

WORKDIR /app
COPY src/ /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
