FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install \
    --default-timeout=1000 \
    --retries=10 \
    --no-cache-dir \
    torch \
    --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install \
    --default-timeout=1000 \
    --retries=10 \
    --no-cache-dir \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]