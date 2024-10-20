# Use the official Python image from the DockerHub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install pika

# Run the consumer script
CMD ["python", "./consumer.py"] 
