FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt FIRST (for better caching)
COPY requirements.txt .

# Then copy app code
COPY ./app /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
