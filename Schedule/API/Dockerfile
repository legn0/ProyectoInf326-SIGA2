# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI app will be running on
EXPOSE 8001

# Start the FastAPI app
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8001"]