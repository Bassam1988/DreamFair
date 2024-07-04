#!/bin/bash

# Function to start a Flask service
# start_flask_service() {
#     SERVICE_DIR=$1
#     PORT=$2

#     echo "Starting service in $SERVICE_DIR on port $PORT..."
#     cd $SERVICE_DIR
#     source env/bin/activate
#     nohup flask run --port=$PORT > flask_$PORT.log 2>&1 &
#     echo "Service at $SERVICE_DIR started on port $PORT"
# }

# start_consumer_service() {
#     SERVICE_DIR=$1  
#     SERVICE_NAME=$2  

#     echo "Starting service in $SERVICE_DIR ...for $SERVICE_NAME"
#     cd $SERVICE_DIR
#     source env/bin/activate
#     nohup python3 $SERVICE_DIR > flask_$SERVICE_NAME.log 2>&1 &
#     echo "Service at $SERVICE_DIR started for $SERVICE_NAME"
# }

# Modified function to start a Flask service
start_flask_service() {
    SERVICE_DIR=$1
    PORT=$2

    echo "Starting service in $SERVICE_DIR on port $PORT..."
    cd $SERVICE_DIR
    source env/bin/activate
    nohup flask run --port=$PORT > flask_$PORT.log 2>&1 &
    echo $! > flask_$PORT.pid
    deactivate
    echo "Service at $SERVICE_DIR started on port $PORT"
}

# Modified function to start a consumer service
start_consumer_service() {
    SERVICE_DIR=$1  
    SERVICE_NAME=$2  

    echo "Starting service in $SERVICE_DIR ...for $SERVICE_NAME"
    cd $SERVICE_DIR
    source env/bin/activate
    nohup python3 $SERVICE_DIR/consumer.py > flask_$SERVICE_NAME.log 2>&1 &
    echo $! > flask_$SERVICE_NAME.pid
    deactivate
    echo "Service at $SERVICE_DIR started for $SERVICE_NAME"
}

# start RabbitMQ Container
#cd /home/ubuntu/DreamFair/DreamFair/src/rabbit
#docker compose -f DockerFile.yaml up -d
# Start each service on a different port
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/auth 5000
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/storyboard 5001
start_flask_service /home/ubuntu/DreamFair/DreamFair/src/gateway 8000


start_consumer_service /home/ubuntu/DreamFair/DreamFair/src/storyboard storyboard
start_consumer_service /home/ubuntu/DreamFair/DreamFair/src/text_to_image_service t2m_consumer
start_consumer_service /home/ubuntu/DreamFair/DreamFair/src/text_to_text_service t2t_consumer

echo "All services have been started."



