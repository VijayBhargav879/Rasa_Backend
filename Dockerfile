FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install rasa==3.12.1 && pip install -U pip && apt-get update && apt-get install -y nginx

# Copy all bot and action files
COPY . /app

# Install action requirements
RUN pip install --no-cache-dir -r actions/requirements.txt

# Copy NGINX config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Start all services
CMD ["sh", "-c", "rasa run --enable-api --cors '*' --port 5005 & rasa run actions --port 5055 & nginx -g 'daemon off;'"]
