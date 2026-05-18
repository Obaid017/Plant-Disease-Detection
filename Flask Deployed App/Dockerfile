# Base image layer with Python runtime environment 
FROM python:3.10-slim

# Set internal isolated workspace directory 
WORKDIR /app

# Copy dependency file layer 
COPY requirements.txt .

# Install application package requirements 
RUN pip install --no-cache-dir -r requirements.txt

# Copy all local folder contents into the container workspace 
COPY . .

# Expose port 7860 for incoming cloud traffic routing
EXPOSE 7860

# Default runtime command to boot up the backend system 
CMD ["python", "app.py"]