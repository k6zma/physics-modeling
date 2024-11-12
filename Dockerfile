FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8051

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8051", "--server.address=0.0.0.0"]
