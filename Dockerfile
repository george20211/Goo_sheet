FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn --timeout 0 --workers 2 --worker-connections=10 google_service.wsgi:application --bind 0:8000