
import os
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from app.models import TrashSubmission
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import LoginForm
from app.models import User, TrashSubmission  # Add TrashSubmission here
from app import db
import threading
import paho.mqtt.client as mqtt
import time




# MQTT setup
message_history = []
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

def start_mqtt_thread():
    thread = threading.Thread(target=mqtt_thread)
    thread.daemon = True  # Ensure the thread stops when the main program exits
    thread.start()
    print("MQTT thread started.")




bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# API route to fetch the latest MQTT message
@bp.route('/latest')
def latest():
    if message_history:
        return jsonify(message=message_history[-1])
    else:
        return jsonify(message="No messages received yet.")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/submit_trash', methods=['GET', 'POST'])
@login_required
def submit_trash():
    if request.method == 'POST':
        image_data = request.form['image_data']
        trash_type = request.form['trash_type']



        if len(message_history) >= 5:
            avg_value = sum(message_history) / len(message_history)
            weight = float(avg_value)
        else:
            weight = 0.00





        manual_trash_type = request.form.get('manual_trash_type')

        # Save the image
        image_path = save_image(image_data)

        # Create a new TrashSubmission
        submission = TrashSubmission(
            user_id=current_user.id,
            image_path=image_path,
            trash_type=manual_trash_type or trash_type,
            weight=weight
        )
        db.session.add(submission)
        db.session.commit()

        return redirect(url_for('main.user_history'))

    return render_template('submit_trash.html')

def save_image(image_data):
    # Remove the data URL prefix
    image_data = image_data.split(',')[1]
    
    # Decode the base64 image data
    import base64
    image_binary = base64.b64decode(image_data)
    
    # Generate a unique filename
    filename = secure_filename(f"{current_user.id}_{int(time.time())}.jpg")
    
    # Save the image to a folder (you may need to create this folder)
    image_path = os.path.join('app', 'static', 'trash_images', filename)
    with open(image_path, 'wb') as f:
        f.write(image_binary)
    
    # Return the relative path to be stored in the database
    return f'/static/trash_images/{filename}'

@bp.route('/user_history')
@login_required
def user_history():
    submissions = current_user.submissions.order_by(TrashSubmission.timestamp.desc()).all()
    return render_template('user_history.html', submissions=submissions)