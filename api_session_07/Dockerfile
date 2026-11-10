FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m app
USER app

EXPOSE 5000
CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 app:app"]
