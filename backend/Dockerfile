# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# --- NEW: Install MySQL client for backups ---
RUN apt-get update && apt-get install -y default-mysql-client

# Copy requirements and the SSL certificate first to leverage caching
COPY requirements.txt .
COPY DigiCertGlobalRootG2.crt.pem .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# The command to run the application using the port from Railway
CMD uvicorn main:app --host 0.0.0.0 --port $PORT