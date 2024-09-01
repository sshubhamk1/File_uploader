FROM python:3.11-slim

WORKDIR /shubhapp

COPY . /shubhapp/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP="./webapp" 
ENV FLASK_ENV="development" 
ENV FLASK_RUN_PORT=8000 
ENV FLASK_RUN_HOST="0.0.0.0"

CMD ["python3", "-m", "flask", "run"]