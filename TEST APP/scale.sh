#!/bin/bash

# MQTT broker and topic configuration
MQTT_BROKER="broker.hivemq.com"  # Replace with your broker if needed
MQTT_PORT=1883
MQTT_TOPIC="test/scale"

# Function to simulate scale readings
simulate_scale() {
    while true; do
        # Generate a random weight between 50 and 150 kg (for example)
        weight=$(awk -v min=50 -v max=150 'BEGIN{srand(); print min+rand()*(max-min)}')

        # Format the weight to 2 decimal places
        weight=$(printf "%.2f" $weight)

        # Publish the weight to the MQTT topic
        mosquitto_pub -h $MQTT_BROKER -p $MQTT_PORT -t $MQTT_TOPIC -m "$weight"

        echo "Published weight: $weight kg to topic: $MQTT_TOPIC"

        # Wait for 5 seconds before publishing the next reading
        sleep 1
    done
}

# Start the scale simulation
simulate_scale
