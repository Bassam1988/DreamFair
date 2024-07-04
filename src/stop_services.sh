#!/bin/bash

# Function to stop a Flask service using its stored PID
stop_flask_service() {
    PORT=$1
    PID_FILE="flask_$PORT.pid"

    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        echo "Stopping Flask service on port $PORT with PID $PID..."
        kill $PID
        rm $PID_FILE
        echo "Service on port $PORT stopped."
    else
        echo "No PID file found for port $PORT. Service might not be running."
    fi
}

# Function to stop a consumer service using its stored PID
stop_consumer_service() {
    SERVICE_NAME=$1
    PID_FILE="flask_$SERVICE_NAME.pid"

    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        echo "Stopping consumer service $SERVICE_NAME with PID $PID..."
        kill $PID
        rm $PID_FILE
        echo "Service $SERVICE_NAME stopped."
    else
        echo "No PID file found for $SERVICE_NAME. Service might not be running."
    fi
}

# Stop Flask services
stop_flask_service 5000
stop_flask_service 5001
stop_flask_service 8000

# Stop consumer services
stop_consumer_service storyboard
stop_consumer_service t2m_consumer
stop_consumer_service t2t_consumer

echo "All services have been stopped."
