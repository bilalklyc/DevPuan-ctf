FROM python:3.11-slim

RUN useradd -m ctfuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R ctfuser:ctfuser /app

EXPOSE 5000
USER ctfuser

CMD ["python", "app.py"]