FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p chroma_db cache data/precedents

EXPOSE 7860

ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV DEBUG=False

HEALTHCHECK CMD curl --fail http://localhost:7860/api/health || exit 1

CMD ["python", "api.py"]
