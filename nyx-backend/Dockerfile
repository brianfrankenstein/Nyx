# Start from a slim Python base image
FROM python:3.11-slim

# Set working directory (creates it if doesn't exist)
WORKDIR /nyx

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project contents into the container
COPY . .

ENV PYTHONPATH=/nyx

# Command to start Nyx (adjust to your actual entry point)
CMD ["python", "src/main.py"]
