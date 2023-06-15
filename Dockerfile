FROM python:3-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Create and activate the virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Add a cron job to execute the script every hour
RUN echo "0 * * * * root /app/venv/bin/python /app/dameon.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron
RUN touch /var/log/cron.log

# Set the command to start cron and tail the log file
CMD service cron start && tail -f /var/log/cron.log
