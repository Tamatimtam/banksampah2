from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
import threading
from tinydb import TinyDB, Query

app = Flask(__name__)

# NoSQL database setup
db = TinyDB('mqtt_data.json')

# Global list to store the last 5 MQTT messages
message_history = []

# MQTT setup
mqtt_broker = "broker.hivemq.com"  # You can replace this with your broker
mqtt_topic = "test/scale"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    global message_history
    message = float(msg.payload.decode())
    
    # Keep only the last 5 messages
    message_history.append(message)
    if len(message_history) > 5:
        message_history.pop(0)

    print(f"Received message: {message}")

# Start the MQTT client in a separate thread
def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, 1883, 60)
    client.loop_forever()

# Route to serve the web page
@app.route('/')
def index():
    return render_template('index.html')

# API route to fetch the latest MQTT message
@app.route('/latest')
def latest():
    if message_history:
        return jsonify(message=message_history[-1])
    else:
        return jsonify(message="No messages received yet.")

# API route to save the average of the last 5 messages
@app.route('/save_average', methods=['POST'])
def save_average():
    if len(message_history) >= 5:
        avg_value = sum(message_history) / len(message_history)
        db.insert({'average': avg_value})
        return jsonify(status="success", average=avg_value)
    else:
        return jsonify(status="error", message="Not enough data to calculate average.")

if __name__ == '__main__':
    # Start the MQTT thread
    threading.Thread(target=mqtt_thread).start()
    
    # Start the Flask app
    app.run(debug=True)
