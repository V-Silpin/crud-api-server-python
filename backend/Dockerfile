# Use official Python image
FROM python:3.11-slim

# Install PostgreSQL client and server
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code (including .env file)
COPY . .

# Set up PostgreSQL with credentials from .env file
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';" && \
    createdb -O postgres appdb

# Switch back to root user
USER root

# Create a startup script that loads environment variables
RUN echo '#!/bin/bash\n\
# Load environment variables from .env file\n\
if [ -f .env ]; then\n\
    export $(cat .env | grep -v "^#" | xargs)\n\
fi\n\
# Update DB_HOST to localhost since PostgreSQL runs in same container\n\
export DB_HOST=localhost\n\
service postgresql start\n\
exec "$@"' > /entrypoint.sh && \
chmod +x /entrypoint.sh

# Expose the backend port and PostgreSQL port
EXPOSE 8000 5432

# Start the backend server (adjust if using something other than uvicorn)
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "main.py"]
