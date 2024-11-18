FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

EXPOSE 8030

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8030"]