from app import create_app, db
from app.routes import start_mqtt_thread
from app.models import User
import threading
from app import create_app, socketio

# Create the Flask app
app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin")
            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()
    
    print("Initialized the database and created default admin user.")

if __name__ == '__main__':
    start_mqtt_thread()
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5000)
