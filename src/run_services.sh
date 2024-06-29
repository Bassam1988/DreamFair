#!/bin/bash

# Function to start a Flask service
start_flask_service() {
    SERVICE_DIR=$1
    PORT=$2

    echo "Starting service in $SERVICE_DIR on port $PORT..."
    cd $SERVICE_DIR
    source env/bin/activate
    nohup flask run --port=$PORT > flask_$PORT.log 2>&1 &
    echo "Service at $SERVICE_DIR started on port $PORT"
}

start_consumer_service() {
    SERVICE_DIR=$1    

    echo "Starting service in $SERVICE_DIR on port $PORT..."
    cd $SERVICE_DIR
    source env/bin/activate
    nohup python $PORT > flask_$PORT.log 2>&1 &
    echo "Service at $SERVICE_DIR started on port $PORT"
}

# start RabbitMQ Container
cd /home/ubuntu/DreamFair/DreamFair/src/rabbit
docker compose -f DockerFile.yaml up -d
# Start each service on a different port
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/auth 5000
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/storyboard 5001
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/gateway 8000

echo "All services have been started."
