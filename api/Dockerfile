FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /api

COPY api/* .
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api

EXPOSE 8000
CMD ["python", "app.py"]