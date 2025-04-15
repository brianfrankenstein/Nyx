# Start from a slim Python base image
FROM python:3.11-slim

# Set working directory (creates it if doesn't exist)
WORKDIR /nyx

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project contents into the container
COPY . .

ENV PYTHONPATH=/nyx

# Ensure you're listening on port 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
