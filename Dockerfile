FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY network_monitor.py .
COPY config.json .

# Create logs directory
RUN mkdir -p /app/logs

# Set entrypoint
ENTRYPOINT ["python", "network_monitor.py"]
CMD ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
