FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 DB_PATH=/data/feedback.db
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY templates templates
RUN mkdir /data
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
