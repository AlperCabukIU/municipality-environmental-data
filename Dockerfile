FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY data/ ./data/
COPY scripts/ ./scripts/

CMD ["python", "scripts/import_data.py"]