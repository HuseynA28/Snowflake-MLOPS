# Use an official Python runtime as a parent image
FROM python:3.11-slim
WORKDIR /app
COPY main.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]