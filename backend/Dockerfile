# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the backend port
EXPOSE 8000

# Start the backend server (adjust if using something other than uvicorn)
CMD ["python", "main.py"]
