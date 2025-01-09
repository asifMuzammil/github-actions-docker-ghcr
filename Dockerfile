# Use official Python image as the base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
